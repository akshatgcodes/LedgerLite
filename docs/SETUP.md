# Local Setup — LedgerLite

> **Just want to try it?** Use the live demo at [ledgerlite.akshatgcodes.in](https://ledgerlite.akshatgcodes.in) and log in with `demo` / `demo1234`.
> This guide is for running LedgerLite locally or self-hosting it.

---

## Prerequisites

- Python 3.8+
- PostgreSQL, optional. Without it, the app uses a local SQLite file.
- Node.js 20+, only if you want to build the landing page

---

## 1. Clone and install

```bash
git clone https://github.com/akshatgcodes/LedgerLite
cd LedgerLite
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 2. Environment variables

Copy `.env.example` to `.env`. `python-dotenv` loads it automatically.

```bash
cp .env.example .env
```

| Variable | Where to get it |
|---|---|
| `DATABASE_URL` | Optional locally. A Postgres URL, for example `postgresql://user:pass@localhost:5432/ledgerlite`, or a [Neon](https://neon.tech) connection string. Leave it empty to use SQLite |
| `SECRET_KEY` | Any long random string, for example from `python -c "import secrets; print(secrets.token_urlsafe(32))"` |

---

## 3. Database setup

There's nothing to run. Tables are created on startup by `db.create_all()`.

- **With Postgres:** `createdb ledgerlite`, then set `DATABASE_URL`.
- **Without Postgres:** leave `DATABASE_URL` empty and the app writes `instance/ledgerlite.db`. This fallback is for local development only.

---

## 4. Run locally

```bash
flask --app app run
```

Open `http://localhost:5000`. Locally, `/` redirects straight to login, since the landing page is only built at deploy time. To preview the landing page:

```bash
cd landing && npm install && npm run dev   # http://localhost:3000
```

---

## 5. Deploy to production

See [DEPLOY.md](DEPLOY.md) for production deployment, custom domain and rollback steps.

---

## Testing

There's no automated test suite yet. CI checks that every Python file compiles and that the landing page lints and builds. To check a change by hand: register, add expenses across a few categories, set a cap below one category's spend, and confirm the dashboard shows the right overage and a matching roast line.

---

## Known local-only limitations

- `/` doesn't show the landing page locally. In production `vercel.json` routes it to the static export.
- SQLite is looser about types than Postgres, so test schema-sensitive changes against Postgres before shipping.

---

<div align="center">

<h3>Akshat Gupta</h3>

<a href="https://akshatgcodes.in"><img src="https://img.shields.io/badge/Website-akshatgcodes.in-111111?style=flat-square&logo=googlechrome&logoColor=white" alt="Website"></a>
<a href="https://linkedin.com/in/akshatgcodes"><img src="https://img.shields.io/badge/LinkedIn-akshatgcodes-0A66C2?style=flat-square" alt="LinkedIn"></a>
<a href="https://github.com/akshatgcodes"><img src="https://img.shields.io/badge/GitHub-akshatgcodes-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"></a>
<a href="mailto:akshatgcodes@gmail.com"><img src="https://img.shields.io/badge/Email-akshatgcodes%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email"></a>

</div>
