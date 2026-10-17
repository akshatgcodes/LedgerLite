<p align="center">
  <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24"
       fill="none" stroke="#1c7c54" stroke-width="1.5"
       stroke-linecap="round" stroke-linejoin="round">
    <path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/>
    <path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>
  </svg>
</p>

<h1 align="center">LedgerLite</h1>

<p align="center">
  <strong>A multi-user expense tracker with monthly budget caps, exact overage math and a spending roast that reads your real numbers.</strong>
</p>

<p align="center">
  <a href="https://ledgerlite.akshatgcodes.in">
    <img src="https://img.shields.io/badge/live_demo-1c7c54-1c7c54?style=flat-square" alt="Live Demo">
  </a>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Next.js-black?style=flat-square&logo=next.js" alt="Next.js">
  <img src="https://img.shields.io/badge/license-GPL--3.0-1c7c54?style=flat-square" alt="License">
</p>

---

## What is LedgerLite?

LedgerLite is an expense tracker for people who want a straight answer about their month, not just a chart. You log what you spend, set a ₹ cap per category, and the dashboard tells you exactly how far over each cap you are. Then it adds a one-line verdict, generated from your own ratios and overages, about where the money actually went.

> **Live demo →** [ledgerlite.akshatgcodes.in](https://ledgerlite.akshatgcodes.in)
> Log in with `demo` / `demo1234`, or create your own account.

---

## What you get

- **Real accounts** — register and log in. Passwords are hashed with bcrypt, and every query is scoped to the signed-in user.
- **Budget caps with overage math** — set a monthly cap per category. Over-budget rows show the exact ₹ amount and percentage over, not just a red flag.
- **Spending roast** — `roast.py` picks between several verdict templates based on what your month actually looks like (blown caps, ₹0 on savings next to heavy fun spend, one category dwarfing another).
- **CSV export** — download all of your own expenses in one click.

---

## Stack

| Layer | Tech |
|---|---|
| Frontend | Jinja2 templates · plain CSS · Next.js 16 static landing page |
| Backend | Python · Flask 3 |
| Database | PostgreSQL (Neon) · Flask-SQLAlchemy · SQLite fallback for local dev |
| Auth | Flask sessions · bcrypt |
| Infra | Vercel (Python function + static landing) · GoDaddy DNS |

---

## Engineering Decisions

**Why a fixed list of categories?**
Free-text categories would make budget caps and the roast's ratio comparisons noisy ("food" vs "Food" vs "groceries"). Ten fixed categories keep every comparison meaningful.

**Why `Decimal` and `Numeric` columns for money?**
Overage math (`spent - cap`) has to be exact to the paisa. Floats would drift; `Numeric(10, 2)` in the database and `Decimal` in Python don't.

**Why is the roast deterministic instead of AI-generated?**
Every verdict is traceable to a computed number (an overage, a ratio, a ₹0 category), so it's never wrong about your data and costs nothing to run.

**What would you do differently in v2?**
Add CSRF protection on every form and move from `db.create_all()` to Alembic migrations. Both were skipped to keep v1 small.

---

## Docs

| Document | Description |
|---|---|
| [PRD](docs/PRD.md) | Product requirements — goals, user stories, non-goals |
| [Architecture](docs/ARCHITECTURE.md) | System design, data flow, component breakdown |
| [Decisions](docs/DECISIONS.md) | Every major technical decision and why |
| [Setup](docs/SETUP.md) | Local dev setup and env vars |
| [Deploy](docs/DEPLOY.md) | Production deployment, domains, rollback |
| [Contributing](CONTRIBUTING.md) | How to propose changes |
| [Changelog](CHANGELOG.md) | What changed in each release |
| [Security](SECURITY.md) | How to report a vulnerability |

---

<div align="center">

<h3>Akshat Gupta</h3>

<a href="https://akshatgcodes.in"><img src="https://img.shields.io/badge/Website-akshatgcodes.in-111111?style=flat-square&logo=googlechrome&logoColor=white" alt="Website"></a>
<a href="https://linkedin.com/in/akshatgcodes"><img src="https://img.shields.io/badge/LinkedIn-akshatgcodes-0A66C2?style=flat-square" alt="LinkedIn"></a>
<a href="https://github.com/akshatgcodes"><img src="https://img.shields.io/badge/GitHub-akshatgcodes-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"></a>
<a href="mailto:akshatgcodes@gmail.com"><img src="https://img.shields.io/badge/Email-akshatgcodes%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email"></a>

</div>
