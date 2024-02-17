"""
LedgerLite -- a multi-user expense tracker with budget caps and a monthly
"spending roast".

Run:
    pip install -r requirements.txt
    flask run

See README.md for PostgreSQL (production) and SQLite (local dev fallback)
setup instructions.
"""

import csv
import io
import re
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from functools import wraps

import bcrypt
from dotenv import load_dotenv
from flask import (
    Flask, render_template, request, redirect, url_for, session, flash,
    Response,
)

load_dotenv()  # picks up DATABASE_URL / SECRET_KEY from a .env file if present

from config import Config
from models import db, User, Expense, Budget, CATEGORIES
from roast import generate_roast

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)
    return app


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def current_user():
    user_id = session.get("user_id")
    if user_id is None:
        return None
    return db.session.get(User, user_id)


def hash_password(plain: str) -> bytes:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt())


def check_password(plain: str, hashed: bytes) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), bytes(hashed))
    except (ValueError, TypeError):
        return False


def parse_amount(raw: str):
    """Returns (Decimal, error_message). error_message is None on success."""
    if raw is None or raw.strip() == "":
        return None, "Amount is required."
    try:
        amount = Decimal(raw.strip())
    except InvalidOperation:
        return None, "Amount must be a valid number."
    if amount <= 0:
        return None, "Amount must be greater than zero."
    if amount > Decimal("1000000000"):
        return None, "Amount is unreasonably large."
    return amount, None


def parse_date(raw: str):
    if not raw:
        return date.today(), None
    try:
        return datetime.strptime(raw.strip(), "%Y-%m-%d").date(), None
    except ValueError:
        return None, "Date must be in YYYY-MM-DD format."


def month_bounds(year: int, month: int):
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, month + 1, 1)
    return start, end


def spend_by_category_for_month(user_id, year, month):
    start, end = month_bounds(year, month)
    rows = (
        db.session.query(Expense.category, db.func.sum(Expense.amount))
        .filter(
            Expense.user_id == user_id,
            Expense.date >= start,
            Expense.date < end,
        )
        .group_by(Expense.category)
        .all()
    )
    return {cat: Decimal(total) for cat, total in rows}


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------

def register_routes(app):

    @app.route("/")
    def index():
        if current_user():
            return redirect(url_for("dashboard"))
        return redirect(url_for("login"))

    # ---- Auth -----------------------------------------------------------

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user():
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            email = (request.form.get("email") or "").strip().lower()
            password = request.form.get("password") or ""
            confirm = request.form.get("confirm_password") or ""

            errors = []
            if len(username) < 3:
                errors.append("Username must be at least 3 characters.")
            if not EMAIL_RE.match(email):
                errors.append("Please enter a valid email address.")
            if len(password) < 6:
                errors.append("Password must be at least 6 characters.")
            if password != confirm:
                errors.append("Passwords do not match.")
            if errors:
                for e in errors:
                    flash(e, "error")
                return render_template("register.html", username=username, email=email)

            if User.query.filter_by(username=username).first():
                flash("That username is already taken.", "error")
                return render_template("register.html", username=username, email=email)
            if User.query.filter_by(email=email).first():
                flash("An account with that email already exists.", "error")
                return render_template("register.html", username=username, email=email)

            user = User(username=username, email=email, password_hash=hash_password(password))
            db.session.add(user)
            db.session.commit()

            flash("Account created. Please log in.", "success")
            return redirect(url_for("login"))

        return render_template("register.html", username="", email="")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user():
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""

            user = User.query.filter_by(username=username).first()
            if user is None or not check_password(password, user.password_hash):
                flash("Invalid username or password.", "error")
                return render_template("login.html", username=username)

            session.clear()
            session["user_id"] = user.id
            flash(f"Welcome back, {user.username}.", "success")
            return redirect(url_for("dashboard"))

        return render_template("login.html", username="")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Logged out.", "success")
        return redirect(url_for("login"))

    # ---- Dashboard --------------------------------------------------------

    @app.route("/dashboard")
    @login_required
    def dashboard():
        user = current_user()
        today = date.today()
        year, month = today.year, today.month

        spend = spend_by_category_for_month(user.id, year, month)
        budgets = {b.category: Decimal(b.monthly_cap) for b in Budget.query.filter_by(user_id=user.id).all()}

        breakdown = []
        total_spent = Decimal("0")
        for cat in CATEGORIES:
            spent = spend.get(cat, Decimal("0"))
            if spent == 0 and cat not in budgets:
                continue
            total_spent += spent
            cap = budgets.get(cat)
            over_amount = None
            pct_of_cap = None
            if cap is not None and cap > 0:
                pct_of_cap = float((spent / cap) * 100)
                if spent > cap:
                    over_amount = spent - cap
            breakdown.append({
                "category": cat,
                "spent": spent,
                "cap": cap,
                "over_amount": over_amount,
                "pct_of_cap": pct_of_cap,
            })

        breakdown.sort(key=lambda r: r["spent"], reverse=True)

        roast = generate_roast(spend, budgets)

        recent_expenses = (
            Expense.query.filter_by(user_id=user.id)
            .order_by(Expense.date.desc(), Expense.id.desc())
            .limit(10)
            .all()
        )

        return render_template(
            "dashboard.html",
            user=user,
            breakdown=breakdown,
            total_spent=total_spent,
            roast=roast,
            recent_expenses=recent_expenses,
            month_name=today.strftime("%B %Y"),
        )

    # ---- Expenses -----------------------------------------------------------

    @app.route("/expenses/add", methods=["GET", "POST"])
    @login_required
    def add_expense():
        user = current_user()

        if request.method == "POST":
            amount, amount_err = parse_amount(request.form.get("amount"))
            category = (request.form.get("category") or "").strip()
            expense_date, date_err = parse_date(request.form.get("date"))
            note = (request.form.get("note") or "").strip()[:255]

            errors = []
            if amount_err:
                errors.append(amount_err)
            if category not in CATEGORIES:
                errors.append("Please choose a valid category.")
            if date_err:
                errors.append(date_err)

            if errors:
                for e in errors:
                    flash(e, "error")
                return render_template(
                    "add_expense.html", categories=CATEGORIES,
                    form={"amount": request.form.get("amount", ""), "category": category,
                          "date": request.form.get("date", ""), "note": note},
                )

            expense = Expense(user_id=user.id, amount=amount, category=category,
                               date=expense_date, note=note or None)
            db.session.add(expense)
            db.session.commit()
            flash("Expense added.", "success")
            return redirect(url_for("dashboard"))

        return render_template(
            "add_expense.html", categories=CATEGORIES,
            form={"amount": "", "category": "", "date": date.today().isoformat(), "note": ""},
        )

    @app.route("/expenses")
    @login_required
    def list_expenses():
        user = current_user()
        expenses = (
            Expense.query.filter_by(user_id=user.id)
            .order_by(Expense.date.desc(), Expense.id.desc())
            .all()
        )
        return render_template("expenses.html", expenses=expenses)

    @app.route("/expenses/<int:expense_id>/delete", methods=["POST"])
    @login_required
    def delete_expense(expense_id):
        user = current_user()
        expense = Expense.query.filter_by(id=expense_id, user_id=user.id).first()
        if expense is None:
            flash("Expense not found.", "error")
        else:
            db.session.delete(expense)
            db.session.commit()
            flash("Expense deleted.", "success")
        return redirect(url_for("list_expenses"))

    # ---- Budgets -----------------------------------------------------------

    @app.route("/budgets", methods=["GET", "POST"])
    @login_required
    def budgets():
        user = current_user()

        if request.method == "POST":
            category = (request.form.get("category") or "").strip()
            cap_amount, cap_err = parse_amount(request.form.get("monthly_cap"))

            errors = []
            if category not in CATEGORIES:
                errors.append("Please choose a valid category.")
            if cap_err:
                errors.append(cap_err)

            if errors:
                for e in errors:
                    flash(e, "error")
            else:
                existing = Budget.query.filter_by(user_id=user.id, category=category).first()
                if existing:
                    existing.monthly_cap = cap_amount
                    flash(f"Updated budget cap for {category}.", "success")
                else:
                    db.session.add(Budget(user_id=user.id, category=category, monthly_cap=cap_amount))
                    flash(f"Set budget cap for {category}.", "success")
                db.session.commit()
            return redirect(url_for("budgets"))

        existing_budgets = {b.category: b for b in Budget.query.filter_by(user_id=user.id).all()}
        return render_template("budgets.html", categories=CATEGORIES, existing_budgets=existing_budgets)

    @app.route("/budgets/<int:budget_id>/delete", methods=["POST"])
    @login_required
    def delete_budget(budget_id):
        user = current_user()
        budget = Budget.query.filter_by(id=budget_id, user_id=user.id).first()
        if budget is None:
            flash("Budget not found.", "error")
        else:
            db.session.delete(budget)
            db.session.commit()
            flash("Budget cap removed.", "success")
        return redirect(url_for("budgets"))

    # ---- CSV export ---------------------------------------------------------

    @app.route("/export")
    @login_required
    def export_csv():
        user = current_user()
        expenses = (
            Expense.query.filter_by(user_id=user.id)
            .order_by(Expense.date.desc(), Expense.id.desc())
            .all()
        )

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["date", "category", "amount", "note"])
        for e in expenses:
            writer.writerow([e.date.isoformat(), e.category, str(e.amount), e.note or ""])

        response = Response(buffer.getvalue(), mimetype="text/csv")
        filename = f"ledgerlite_{user.username}_{date.today().isoformat()}.csv"
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        return response


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

# Built incrementally - see git history for the development progression.
