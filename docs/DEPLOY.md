# Deploying LedgerLite

> **Live:** [ledgerlite.akshatgcodes.in](https://ledgerlite.akshatgcodes.in) · **Host:** Vercel · **Auto-deploy:** on push to `master`

For local development, see [SETUP.md](SETUP.md).

---

## 1. Architecture in production

| Piece | Runs on | Notes |
|---|---|---|
| Landing page | Vercel (static) | `landing/` built with `@vercel/static-build`, served at `/` |
| Flask app | Vercel (Python function) | `app.py` through `@vercel/python`; handles every route except `/`, `/_next/*`, `/favicon.ico` and `/static/*` |
| Database | Neon Postgres | Free tier, `aws-ap-southeast-1`; compute sleeps after 5 min idle |
| DNS | GoDaddy | `ledgerlite.akshatgcodes.in` → CNAME to Vercel |

---

## 2. Environment variables

Set these in Vercel → Project `ledgerlite` → Settings → Environment Variables (Production and Preview). Names are in [`.env.example`](../.env.example).

| Variable | Required | Where it's set |
|---|---|---|
| `DATABASE_URL` | ✅ | Vercel env vars. Neon connection string |
| `SECRET_KEY` | ✅ | Vercel env vars. Long random string; changing it logs everyone out |

> After changing an env var, **redeploy**. Running deployments don't pick up new values.

---

## 3. First-time deploy

1. [vercel.com/new](https://vercel.com/new) → import `akshatgcodes/LedgerLite`
2. Framework preset: **Other** · Root directory: `./` (the repo's `vercel.json` defines the builds)
3. Add the env vars from section 2
4. Deploy. Every push to `master` now deploys to production, and every PR gets a preview URL.

`vercel.json` does the routing:

```json
{ "src": "/",            "dest": "/landing/index.html" },
{ "src": "/_next/(.*)",  "dest": "/landing/_next/$1" },
{ "src": "/static/(.*)", "dest": "/static/$1" },
{ "src": "/(.*)",        "dest": "/app.py" }
```

---

## 4. Database migrations

There's no migration tool. `db.create_all()` runs on every cold start and creates any missing tables. It never alters existing ones, so a schema change needs Alembic (or a manual `ALTER TABLE`) first.

---

## 5. Custom domain

`ledgerlite.akshatgcodes.in` is set up with the setup toolkit:

```powershell
.\scripts\setup-subdomain.ps1 -Subdomain "ledgerlite" -Platform Vercel -VercelProject "ledgerlite"
```

Manual fallback: add the domain in Vercel → Project → Domains, then create a GoDaddy CNAME `ledgerlite` → the target Vercel shows. HTTPS certificates are issued automatically once DNS resolves (2–10 min).

---

## 6. Verify a deploy

- [ ] `https://ledgerlite.akshatgcodes.in` loads the landing page
- [ ] `/register` and `/login` load, and logging in with `demo` / `demo1234` reaches the dashboard
- [ ] Adding an expense shows it on the dashboard with the right total
- [ ] `/export` downloads a CSV

---

## 7. Rollback

| Host | How |
|---|---|
| Vercel | Dashboard → Deployments → pick the last good one → **Promote to Production** (or `vercel rollback`) |
| Database | Neon → Branches → restore from a point in time |

After rolling back, note it in a commit or PR so the next push doesn't silently re-ship the broken version.

---

## 8. Monitoring & logs

- **Logs:** Vercel → Project `ledgerlite` → Logs
- **Errors:** none yet beyond Vercel's function logs
- **Uptime:** none yet
- **Dependencies:** Dependabot opens weekly update PRs and a maintenance report is emailed every week (see `.github/workflows/`)

---

## Known production limitations

- The first request after Neon has been idle for 5+ minutes is slower while the database wakes up.
- Vercel prints a warning about the legacy `builds` config on every deploy. It's expected.

---

<div align="center">

<h3>Akshat Gupta</h3>

<a href="https://akshatgcodes.in"><img src="https://img.shields.io/badge/Website-akshatgcodes.in-111111?style=flat-square&logo=googlechrome&logoColor=white" alt="Website"></a>
<a href="https://linkedin.com/in/akshatgcodes"><img src="https://img.shields.io/badge/LinkedIn-akshatgcodes-0A66C2?style=flat-square" alt="LinkedIn"></a>
<a href="https://github.com/akshatgcodes"><img src="https://img.shields.io/badge/GitHub-akshatgcodes-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"></a>
<a href="mailto:akshatgcodes@gmail.com"><img src="https://img.shields.io/badge/Email-akshatgcodes%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email"></a>

</div>
