# LedgerLite — Product Requirements Document

**Status:** Final (v1 shipped)
**Owner:** Akshat Gupta
**One-liner:** A multi-user expense tracker with monthly budget caps, exact overage math and a spending roast that reads your real numbers.

---

## 1. Problem

Most expense trackers stop at a pie chart. You can see that Food was the biggest slice, but not how far past your own limit you went, and nothing tells you plainly that the month went sideways. People who want to stick to a budget need two things a chart doesn't give them: the exact amount they're over, and a blunt summary they can't scroll past.

---

## 2. Goals (v1)

1. Separate accounts: each user registers, logs in, and only ever sees their own data.
2. Log an expense with an amount, a category from a fixed list, a date and an optional note.
3. Set one monthly ₹ cap per category and see the exact amount and percentage over the cap for the current month.
4. Show a one-line verdict on the dashboard that is computed from the current month's numbers.
5. Export all of a user's expenses as CSV.
6. Live, usable demo at [ledgerlite.akshatgcodes.in](https://ledgerlite.akshatgcodes.in).

---

## 3. Non-Goals (explicit scope cuts)

- **Custom categories** — a fixed list of ten keeps caps and ratio comparisons meaningful. Free-text would need normalisation.
- **Past-month dashboards** — the dashboard covers the current calendar month only. The expense list and CSV export still include everything.
- **Multiple currencies** — amounts are ₹ only.
- **Bank sync / receipt scanning** — manual entry only; the point is the budgeting feedback, not data ingestion.
- **Charts** — the category table with overage rows replaces a chart in v1.

---

## 4. Users

**Primary:** Students and early-career earners who want to stick to a monthly budget and like a blunt nudge.

**Secondary:** Recruiters and engineers reviewing this as a portfolio piece. They need to log in and see a populated dashboard in under a minute, so there's a demo account.

---

## 5. User Stories

1. *As a new user,* I register with a username, email and password so that my expenses are private to me.
2. *As a user,* I add an expense with an amount, category, date and note so that my month is recorded.
3. *As a user,* I set a monthly cap for Food so that I know when I'm overspending on it.
4. *As a user,* I open the dashboard and see each category's spend, cap and exact overage so that I know where I stand.
5. *As a user,* I read the roast line so that I get an honest one-sentence summary of my month.
6. *As a user,* I delete a mistaken expense or remove a cap so that the numbers stay correct.
7. *As a user,* I export my expenses to CSV so that I can analyse them elsewhere.

---

## 6. Functional Requirements

### 6.1 Auth

- Registration requires a username of 3+ characters, a valid email and a password of 6+ characters, entered twice.
- Usernames and emails are unique.
- Passwords are stored as bcrypt hashes only.
- Every page except register and login redirects to login when there's no session.

### 6.2 Expenses

- Amount must be a number greater than 0 and no more than ₹1,000,000,000.
- Category must be one of: Food, Rent, Transport, Subscriptions, Entertainment, Shopping, Utilities, Health, Savings, Other.
- Date defaults to today and must be `YYYY-MM-DD`.
- A user can delete only their own expenses.

### 6.3 Budgets

- One cap per user per category (enforced by a unique constraint). Setting it again updates it.
- A user can remove only their own caps.

### 6.4 Dashboard

- Shows the current month's spend per category, sorted by amount, including categories with a cap but no spend.
- For a category over its cap, shows the over amount (`spent - cap`) and percentage of cap, and highlights the row.
- Shows the 10 most recent expenses and the month's total.
- Shows one roast line (see [ARCHITECTURE.md](ARCHITECTURE.md#5-roast-engine)).

### 6.5 Export

- `GET /export` returns a CSV of the signed-in user's expenses (`date, category, amount, note`), newest first.

---

## 7. Non-Functional Requirements

- **Correctness:** Money uses `Decimal` / `Numeric(10, 2)` end to end. No floats in stored values or overage math.
- **Security:** Passwords hashed with bcrypt. Every expense and budget query filters by the session's `user_id`. Secrets (`SECRET_KEY`, `DATABASE_URL`) come from env vars only.
- **Cost:** Runs on free tiers (Vercel + Neon). No paid APIs.
- **Portability:** Same code runs on PostgreSQL in production and SQLite locally.

---

## 8. Success Metrics

| Metric | Target |
|---|---|
| Live demo reliability | Landing page → logged-in dashboard with the demo account in under 30 seconds |
| Data isolation | No route returns or modifies another user's rows |
| Roast relevance | Every roast line references a real category or amount from the user's month |

---

## 9. Risks & Open Questions

- **No CSRF protection** — forms rely on the session cookie alone. Acceptable for a demo; should be fixed before real use.
- **Schema changes** — tables are created with `db.create_all()`, which can't alter existing tables. Any schema change needs a migration tool first.
- **Shared demo account** — anyone can edit the demo data, so it may look messy at times.

---

## 10. v2 Candidates

- CSRF tokens on every form (Flask-WTF) — first thing to add before real users.
- Month picker on the dashboard — the queries already take a year and month.
- Alembic migrations — needed before the first schema change.
- Automated tests for `roast.py` — it's pure logic and easy to unit-test.

---

<div align="center">

<h3>Akshat Gupta</h3>

<a href="https://akshatgcodes.in"><img src="https://img.shields.io/badge/Website-akshatgcodes.in-111111?style=flat-square&logo=googlechrome&logoColor=white" alt="Website"></a>
<a href="https://linkedin.com/in/akshatgcodes"><img src="https://img.shields.io/badge/LinkedIn-akshatgcodes-0A66C2?style=flat-square" alt="LinkedIn"></a>
<a href="https://github.com/akshatgcodes"><img src="https://img.shields.io/badge/GitHub-akshatgcodes-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"></a>
<a href="mailto:akshatgcodes@gmail.com"><img src="https://img.shields.io/badge/Email-akshatgcodes%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email"></a>

</div>
