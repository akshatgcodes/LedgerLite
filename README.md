# LedgerLite

A multi-user expense tracker built with Flask, Flask-SQLAlchemy, and PostgreSQL. Register, log in, log expenses by category and date, set monthly budget caps, view a dashboard with budget-overage warnings, and get roasted for your spending habits at the end of the month.

## The X Factor

**Spending roast.** Every time you load the dashboard, LedgerLite analyzes your current month's category breakdown and procedurally generates a one-liner verdict about your spending. It's not one canned string — `roast.py` computes real ratios and overage amounts from your data and picks between several distinct templates depending on what it finds:

- A category badly exceeding its budget cap (e.g. "You blew past your Food budget by ₹1,200.00 (60% over cap). Bold move.")
- Zero spend on a "responsible" category (Savings, Rent, Utilities, Health) next to heavy spend on a "fun" one (e.g. "₹0 on Savings, ₹4,200.00 on Subscriptions — bold strategy.")
- One category dwarfing another by 3x or more (e.g. "You spent 3x more on Food than Rent. Priorities?")
- One category eating over half your total monthly spend
- A milder over-budget nudge, or a neutral "here's what you actually spent on" fallback if nothing dramatic stands out

**Budget caps with real overage math.** Set a monthly ₹ cap per category on the Budgets page. The dashboard doesn't just flag "over budget" with a boolean — it computes and displays the exact amount and percentage you're over, and highlights that row in red.

## Key concepts demonstrated

- **Auth**: Flask sessions for login state, `bcrypt` for password hashing (never plaintext, never a reversible hash)
- **ORM**: Flask-SQLAlchemy models (`User`, `Expense`, `Budget`) with foreign keys, a unique constraint (one budget cap per user per category), and `Decimal`-backed `Numeric` columns for money
- **Budget logic**: per-category monthly aggregation via `SUM(...) GROUP BY category` scoped to the current month, then real overage subtraction (`spent - cap`)
- **Procedural generation**: `roast.py` is pure logic, unit-testable independent of Flask, that picks between multiple templates gated on different ratio/overage/near-zero conditions
- **Validation & UX**: server-side validation for amounts, dates, categories, email format, password length/confirmation, all surfaced via `flash()` messages
- **CSV export**: streamed `text/csv` response built with Python's `csv` module, scoped to the logged-in user only

## Project structure

```
LedgerLite/
├── app.py            # routes, auth, request handling
├── config.py         # DB config (PostgreSQL via DATABASE_URL, SQLite fallback)
├── models.py          # SQLAlchemy models: User, Expense, Budget
├── roast.py           # procedural spending-roast generator (framework-independent)
├── templates/         # Jinja2 templates
├── static/style.css   # styling
├── requirements.txt
└── .gitignore
```

## Running it

### Requirements

- Python 3.8+
- PostgreSQL (intended production database) — or nothing extra for local dev (see SQLite fallback below)

### 1. Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure the database

**Production / intended usage: PostgreSQL.**

Create a database and user, then set `DATABASE_URL` (a `.env` file in the project root works too, thanks to `python-dotenv`):

```bash
createdb ledgerlite
export DATABASE_URL="postgresql+psycopg2://ledgeruser:ledgerpass@localhost:5432/ledgerlite"
```

or in `.env`:

```
DATABASE_URL=postgresql+psycopg2://ledgeruser:ledgerpass@localhost:5432/ledgerlite
SECRET_KEY=some-long-random-string
```

Tables are created automatically on first run via `db.create_all()` (fine for a portfolio project; a real production app would use Flask-Migrate/Alembic instead).

**Local dev / testing fallback: SQLite.**

If `DATABASE_URL` is not set, LedgerLite automatically falls back to a local SQLite file at `instance/ledgerlite.db`. This exists purely so the app's logic (auth, expenses, budget math, roast generation) can be run and tested without a PostgreSQL server available. It is **not** the intended production setup — just point `DATABASE_URL` at Postgres when you have one.

### 3. Run

```bash
export FLASK_APP=app.py
flask run
```

Open `http://localhost:5000`, register an account, and start logging expenses.

## Usage

1. **Register / log in** — passwords are hashed with `bcrypt` before storage.
2. **Add expenses** — amount, category (fixed list: Food, Rent, Transport, Subscriptions, Entertainment, Shopping, Utilities, Health, Savings, Other), date, optional note.
3. **Set budget caps** — on the Budgets page, set a ₹ monthly cap per category.
4. **Dashboard** — see this month's totals by category, red-highlighted rows for any category over its cap (with the exact overage amount), and your monthly roast.
5. **Export CSV** — anytime, from the nav bar or the Expenses page; downloads only your own expenses.

## Notes

Built as a focused, single-purpose tool - a multi-user expense tracker, nothing more, nothing less.
