"""SQLAlchemy models for LedgerLite. Works identically against PostgreSQL and SQLite."""

from datetime import datetime, date

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# A reasonable, fixed set of categories keeps budget caps and the roast
# generator meaningful (free-text categories would make ratio comparisons
# noisy). Users pick from this list when adding expenses / setting budgets.
CATEGORIES = [
    "Food",
    "Rent",
    "Transport",
    "Subscriptions",
    "Entertainment",
    "Shopping",
    "Utilities",
    "Health",
    "Savings",
    "Other",
]


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    expenses = db.relationship("Expense", backref="user", lazy=True, cascade="all, delete-orphan")
    budgets = db.relationship("Budget", backref="user", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    note = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Expense {self.category} {self.amount} on {self.date}>"


class Budget(db.Model):
    """A per-user, per-category monthly budget cap."""

    __tablename__ = "budgets"
    __table_args__ = (
        db.UniqueConstraint("user_id", "category", name="uq_budget_user_category"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False)
    monthly_cap = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f"<Budget {self.category} cap={self.monthly_cap}>"
