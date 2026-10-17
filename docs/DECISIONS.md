# Engineering Decisions — LedgerLite

---

## Decision 1 — A fixed list of ten categories

**Context:** Budget caps and the roast both compare categories against each other. With free-text categories, "food", "Food" and "groceries" would be three different buckets.

**Decision:** A fixed `CATEGORIES` list in `models.py`, used by every form, the dashboard and the roast.

**Reason:** Every cap and every ratio ("3x more on Food than Rent") compares like with like. It also lets the roast group categories into "responsible" and "discretionary" sets.

**Tradeoff:** Users can't add their own categories. Anything that doesn't fit goes to "Other".

---

## Decision 2 — `Decimal` everywhere money is handled

**Context:** The dashboard shows exact overages such as "₹1,200.00 over (60%)". Floating-point maths would produce values like `1199.9999`.

**Decision:** `Numeric(10, 2)` columns, `Decimal` parsing in `parse_amount()`, and `Decimal` arithmetic in both the dashboard and `roast.py`.

**Reason:** Money has to add up exactly, to the paisa. `Decimal` also makes validation simple: anything that fails `Decimal(raw)` is rejected.

**Tradeoff:** A little more conversion code, for example turning SQL `SUM` results back into `Decimal`.

---

## Decision 3 — A rule-based roast, not an LLM

**Context:** The roast is the app's personality, but it must never misstate the user's money.

**Decision:** `roast.py` checks five ordered patterns against real totals and fills a template with the numbers it found.

**Reason:** Every line is traceable to a computed value, so it's always correct about the data. It runs in microseconds, needs no API key, and costs nothing.

**Tradeoff:** The wording is limited to a few templates per pattern, so heavy users will see repeats.

---

## Decision 4 — Postgres in production, SQLite as a local fallback

**Context:** The app should run with zero setup for someone trying it locally, but production needs a real database.

**Decision:** `config.py` uses `DATABASE_URL` when it's set and falls back to `instance/ledgerlite.db` when it isn't. The URL is normalised to `postgresql+psycopg2://`.

**Reason:** The same SQLAlchemy models work against both. The driver pin was added after a production crash: newer SQLAlchemy maps plain `postgresql://` URLs to psycopg 3, which isn't installed.

**Tradeoff:** SQLite is looser about types than Postgres, so a bug could appear only in production. That's why the deployed app is tested against Neon.

---

## Decision 5 — Landing page and app on one Vercel project

**Context:** The landing page (Next.js) and the app (Flask) used to be deployed separately, which meant two URLs for one project.

**Decision:** One Vercel project. `vercel.json` builds `landing/` as a static export and routes `/` to it, and routes everything else to the Flask function.

**Reason:** One domain (`ledgerlite.akshatgcodes.in`), one deploy per push, and the landing page's buttons go straight to `/register` and `/login`. Vercel's zero-config Flask preset didn't serve build-generated files, so the legacy `builds` + `routes` format is used.

**Tradeoff:** `builds` is Vercel's older config format and shows a warning on deploy.

---

## What I'd do differently in v2

- **CSRF protection** — forms currently trust the session cookie alone. Flask-WTF's CSRF tokens should be on every POST.
- **Migrations** — `db.create_all()` can't alter existing tables. Alembic should be in place before the first schema change.
- **Tests** — `roast.py` and the overage maths are pure functions and should have unit tests.

---

## Explicit non-decisions (deferred to v2)

| Feature | Why deferred |
|---|---|
| Month picker | The dashboard query already takes a year and month. Only the UI is missing |
| Charts | The overage table answers "where am I over?" more directly than a pie chart |
| Custom categories | Would break the roast's category groupings (see Decision 1) |

---

<div align="center">

<h3>Akshat Gupta</h3>

<a href="https://akshatgcodes.in"><img src="https://img.shields.io/badge/Website-akshatgcodes.in-111111?style=flat-square&logo=googlechrome&logoColor=white" alt="Website"></a>
<a href="https://linkedin.com/in/akshatgcodes"><img src="https://img.shields.io/badge/LinkedIn-akshatgcodes-0A66C2?style=flat-square" alt="LinkedIn"></a>
<a href="https://github.com/akshatgcodes"><img src="https://img.shields.io/badge/GitHub-akshatgcodes-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"></a>
<a href="mailto:akshatgcodes@gmail.com"><img src="https://img.shields.io/badge/Email-akshatgcodes%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email"></a>

</div>
