# Changelog

All notable changes to **LedgerLite** are documented here.

---

## [1.0.0] — 2026-10-18

### ✨ Added
- Accounts with registration and login; passwords hashed with bcrypt
- Expenses with amount, category, date and note, plus a list and delete
- Monthly budget caps per category, with the exact amount and percentage over each cap on the dashboard
- Procedural spending roast generated from the month's real numbers
- CSV export of your own expenses
- Next.js landing page, served from the same site as the app with live sign-up and login links

### 🎊 Improved
- Works with any Postgres via `DATABASE_URL`, falling back to SQLite when it isn't set

### 🐛 Fixed
- Production crash on Postgres URLs: the psycopg2 driver is now pinned so newer SQLAlchemy doesn't look for psycopg 3

---

[1.0.0]: https://github.com/akshatgcodes/LedgerLite/releases/tag/v1.0.0

---

<div align="center">

<h3>Akshat Gupta</h3>

<a href="https://akshatgcodes.in"><img src="https://img.shields.io/badge/Website-akshatgcodes.in-111111?style=flat-square&logo=googlechrome&logoColor=white" alt="Website"></a>
<a href="https://linkedin.com/in/akshatgcodes"><img src="https://img.shields.io/badge/LinkedIn-akshatgcodes-0A66C2?style=flat-square" alt="LinkedIn"></a>
<a href="https://github.com/akshatgcodes"><img src="https://img.shields.io/badge/GitHub-akshatgcodes-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"></a>
<a href="mailto:akshatgcodes@gmail.com"><img src="https://img.shields.io/badge/Email-akshatgcodes%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email"></a>

</div>
