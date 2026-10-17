# LedgerLite — Architecture

---

## 1. Stack

| Layer | Tech |
|---|---|
| Framework | Flask 3 (Python 3.12 on Vercel) |
| Auth | Flask signed-cookie sessions · bcrypt |
| Database | PostgreSQL on Neon (production) · SQLite file (local fallback) |
| ORM | Flask-SQLAlchemy · psycopg2 |
| Templates | Jinja2 · plain CSS (`static/style.css`) |
| Landing page | Next.js 16 static export (`landing/`) · Tailwind CSS 4 |
| Hosting | Vercel: `@vercel/python` for Flask, `@vercel/static-build` for the landing page |

---

## 2. Components

```
app.py            Flask app factory, auth helpers, all routes, CSV export
config.py         reads DATABASE_URL / SECRET_KEY, picks Postgres or SQLite
models.py         User, Expense, Budget models + the fixed CATEGORIES list
roast.py          pure-Python roast generator (no Flask imports)
templates/        Jinja2 pages: auth, dashboard, expenses, budgets
static/style.css  app styling
landing/          Next.js landing page, exported to static HTML
vercel.json       routes "/" to the landing page and everything else to Flask
```

### App factory (`app.py`)

`create_app()` loads `Config`, binds Flask-SQLAlchemy, runs `db.create_all()` and registers the routes. A module-level `app = create_app()` is the WSGI entry point Vercel imports.

### Config (`config.py`)

If `DATABASE_URL` is set, it's used after two rewrites: `postgres://` becomes `postgresql://`, and plain `postgresql://` becomes `postgresql+psycopg2://` so SQLAlchemy uses the installed driver. Without it, the app falls back to `instance/ledgerlite.db`.

### Models (`models.py`)

Three tables, all money in `Numeric(10, 2)`. `CATEGORIES` lives here so the forms, the dashboard and the roast all share one list.

### Roast engine (`roast.py`)

`generate_roast(spend, budgets)` takes two dicts of `Decimal`s and returns one string. It has no Flask or database imports, so it can be tested on its own. See section 5.

### Landing page (`landing/`)

A Next.js app with `output: "export"`. At deploy time it becomes static HTML served at `/`, with links to `/register` and `/login`.

---

## 3. Data Flow

```
[Browser] GET /           --> vercel.json --> landing/index.html (static)
[Browser] POST /login     --> Flask: bcrypt check --> session["user_id"]
[Browser] GET /dashboard  --> Flask
      --> SUM(amount) GROUP BY category for this month (user-scoped)
      --> load the user's budget caps
      --> compute spent / cap / over_amount / pct_of_cap per category
      --> generate_roast(spend, caps)
      --> render dashboard.html
```

1. A visitor lands on the static landing page and clicks **Try it live** or **Log in**.
2. Flask checks the bcrypt hash and stores only `user_id` in the signed session cookie.
3. Adding an expense validates amount, category and date, then inserts a row for that user.
4. The dashboard runs one grouped query for the current month, joins it with the caps in Python, and works out each overage.
5. The roast engine gets the same totals and returns one line, which is rendered above the table.

---

## 4. Database Schema

- `users` — `id`, `username` (unique, indexed), `email` (unique, indexed), `password_hash` (bcrypt bytes), `created_at`
- `expenses` — `id`, `user_id` → `users.id` (indexed), `amount` `Numeric(10,2)`, `category` (indexed), `date`, `note`, `created_at`
- `budgets` — `id`, `user_id` → `users.id` (indexed), `category`, `monthly_cap` `Numeric(10,2)`

**Constraints:** `UNIQUE(budgets.user_id, budgets.category)` keeps one cap per category. Deleting a user cascades to their expenses and budgets.

**Indexes:** `expenses(user_id)` and `expenses(category)` serve the dashboard's per-user, per-category monthly sum.

---

## 5. Roast Engine

Patterns are checked in order, and the first one that matches wins. Each has two or more wordings, and one is picked at random.

| # | Pattern | Condition |
|---|---|---|
| 1 | Blown cap | Worst overage is at least 50% over its cap |
| 2 | Priorities | A "responsible" category (Savings, Rent, Utilities, Health) is ₹0 while a discretionary one (Food, Entertainment, Subscriptions, Shopping) is at least 15% of the total |
| 3 | Lopsided | One category is at least 3x another and at least 10% of the total |
| 4 | Dominant | One category is at least 50% of the month |
| 5 | Mild overage | Some category is over its cap, but by less than 50% |
| — | Fallback | Names the biggest category and its share |
| — | No data | No expenses this month |

---

## 6. Routes

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Landing page in production. Locally, redirects to dashboard or login |
| `GET/POST` | `/register` | Create an account |
| `GET/POST` | `/login` | Start a session |
| `GET` | `/logout` | Clear the session |
| `GET` | `/dashboard` | Current month breakdown, overages, roast, recent expenses |
| `GET/POST` | `/expenses/add` | Add an expense |
| `GET` | `/expenses` | All of the user's expenses |
| `POST` | `/expenses/<id>/delete` | Delete one of the user's expenses |
| `GET/POST` | `/budgets` | Set or update a category cap |
| `POST` | `/budgets/<id>/delete` | Remove one of the user's caps |
| `GET` | `/export` | CSV download of the user's expenses |

---

## 7. Security

- **Passwords:** `bcrypt.hashpw` with a fresh salt. A malformed hash makes `checkpw` return false rather than raise.
- **Sessions:** Flask's signed cookie holds only `user_id`. It's signed with `SECRET_KEY`, which comes from an env var in production.
- **Data isolation:** every read, update and delete of expenses and budgets filters by `user_id` from the session, so guessing another row's id returns "not found".
- **Secrets:** `DATABASE_URL` and `SECRET_KEY` are Vercel env vars. `.env*` files are gitignored.
- **Known gap:** there's no CSRF token on forms yet (see [DECISIONS.md](DECISIONS.md)).

---

## 8. Error Handling & Reliability

| Failure | Behaviour |
|---|---|
| Invalid form input | Each problem is flashed and the form re-renders with the user's values |
| Duplicate username / email | Flash message, no insert |
| Deleting someone else's row | Treated as not found, nothing deleted |
| Database unreachable | Request fails with a 500; Vercel logs the traceback |
| Neon compute asleep | First query wakes it, adding a short delay |

---

## 9. Deployment

1. The Vercel project `ledgerlite` is linked to `akshatgcodes/LedgerLite` and deploys every push to `master`.
2. `vercel.json` uses `builds` + `routes`: `landing/` is built with `@vercel/static-build` and served at `/`, `static/**` is served as files, and everything else goes to `app.py` through `@vercel/python`.
3. `DATABASE_URL` (Neon) and `SECRET_KEY` are set in Vercel project env vars.
4. Tables are created on cold start by `db.create_all()`.

Full steps are in [DEPLOY.md](DEPLOY.md).

---

## 10. Explicit Scope Cuts

- **Migrations** — `db.create_all()` instead of Alembic. Fine while the schema is fixed.
- **Month picker** — dashboard is current month only.
- **Charts** — the category table is the visualisation.

---

<div align="center">

<h3>Akshat Gupta</h3>

<a href="https://akshatgcodes.in"><img src="https://img.shields.io/badge/Website-akshatgcodes.in-111111?style=flat-square&logo=googlechrome&logoColor=white" alt="Website"></a>
<a href="https://linkedin.com/in/akshatgcodes"><img src="https://img.shields.io/badge/LinkedIn-akshatgcodes-0A66C2?style=flat-square" alt="LinkedIn"></a>
<a href="https://github.com/akshatgcodes"><img src="https://img.shields.io/badge/GitHub-akshatgcodes-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"></a>
<a href="mailto:akshatgcodes@gmail.com"><img src="https://img.shields.io/badge/Email-akshatgcodes%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email"></a>

</div>
