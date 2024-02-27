const roasts = [
  {
    line: "You spent 3x more on food than rent. Priorities?",
    tag: "Food vs. Rent",
  },
  {
    line: "₹0 on savings, ₹4,200 on subscriptions — bold strategy.",
    tag: "Savings vs. Subscriptions",
  },
  {
    line: "Entertainment ate 41% of your budget this month. The popcorn wasn't that good.",
    tag: "Entertainment share",
  },
];

const categories = [
  { name: "Rent", spent: 18000, cap: 18000, over: false },
  { name: "Food & Dining", spent: 9640, cap: 6000, over: true },
  { name: "Transport", spent: 2100, cap: 3000, over: false },
  { name: "Subscriptions", spent: 4200, cap: 1500, over: true },
  { name: "Savings", spent: 0, cap: 5000, over: false },
];

const concepts = [
  "Flask sessions",
  "bcrypt password hashing",
  "PostgreSQL",
  "Flask-SQLAlchemy",
  "Budget-cap overage logic",
  "Procedural roast generation",
  "Form validation & flash messages",
  "CSV export",
  "Jinja2 templates",
];

function formatINR(n: number) {
  return `₹${n.toLocaleString("en-IN")}`;
}

function GitHubIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" {...props}>
      <path d="M12 .5C5.73.5.75 5.48.75 11.75c0 5.02 3.26 9.28 7.77 10.78.57.1.78-.25.78-.55 0-.27-.01-1.17-.02-2.12-3.16.69-3.83-1.34-3.83-1.34-.52-1.31-1.26-1.66-1.26-1.66-1.03-.7.08-.69.08-.69 1.14.08 1.74 1.17 1.74 1.17 1.01 1.73 2.65 1.23 3.3.94.1-.73.4-1.23.72-1.51-2.52-.29-5.17-1.26-5.17-5.6 0-1.24.44-2.25 1.17-3.04-.12-.29-.51-1.45.11-3.02 0 0 .96-.31 3.14 1.16a10.9 10.9 0 0 1 5.72 0c2.18-1.47 3.14-1.16 3.14-1.16.62 1.57.23 2.73.11 3.02.73.79 1.17 1.8 1.17 3.04 0 4.35-2.65 5.31-5.18 5.59.41.35.77 1.04.77 2.1 0 1.52-.01 2.74-.01 3.11 0 .3.2.66.79.55A11.26 11.26 0 0 0 23.25 11.75C23.25 5.48 18.27.5 12 .5Z" />
    </svg>
  );
}

function Badge({ children }: { children: React.ReactNode }) {
  return (
    <span className="inline-flex items-center rounded-full border border-border bg-surface px-3 py-1 text-xs font-medium text-muted">
      {children}
    </span>
  );
}

export default function Home() {
  return (
    <div className="flex flex-1 flex-col bg-background font-sans">
      {/* Nav */}
      <header className="sticky top-0 z-20 border-b border-border bg-background/85 backdrop-blur">
        <div className="mx-auto flex w-full max-w-5xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-2">
            <span className="flex h-7 w-7 items-center justify-center rounded-md bg-accent text-sm font-bold text-white">
              L
            </span>
            <span className="text-sm font-semibold tracking-tight">
              LedgerLite
            </span>
          </div>
          <nav className="flex items-center gap-6 text-sm text-muted">
            <a href="#roast" className="hidden hover:text-foreground sm:inline">
              The Roast
            </a>
            <a href="#run" className="hidden hover:text-foreground sm:inline">
              Run it
            </a>
            <a
              href="https://github.com"
              className="inline-flex items-center gap-1.5 rounded-md border border-border px-3 py-1.5 font-medium text-foreground transition hover:border-accent hover:text-accent"
            >
              <GitHubIcon className="h-4 w-4" />
              Source
            </a>
          </nav>
        </div>
      </header>

      <main className="flex-1">
        {/* Hero */}
        <section className="mx-auto w-full max-w-5xl px-6 pb-20 pt-16 sm:pt-24">
          <div className="max-w-2xl">
            <Badge>Flask · PostgreSQL · Multi-user</Badge>
            <h1 className="mt-5 text-4xl font-semibold leading-[1.1] tracking-tight sm:text-5xl">
              The expense tracker that keeps a{" "}
              <span className="text-accent">ledger</span> — and an opinion.
            </h1>
            <p className="mt-5 text-lg leading-relaxed text-muted">
              LedgerLite is a multi-user expense tracker with real
              authentication, category breakdowns, and CSV export. Add what
              you spend, set a budget per category, and get a straight
              answer about whether you kept it. Most trackers stop at the
              chart — LedgerLite adds the verdict.
            </p>
            <div className="mt-8 flex flex-wrap items-center gap-3">
              <a
                href="https://github.com"
                className="inline-flex items-center gap-2 rounded-md bg-accent px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-accent-2"
              >
                <GitHubIcon className="h-4 w-4" />
                View on GitHub
              </a>
              <a
                href="#run"
                className="inline-flex items-center gap-2 rounded-md border border-border px-5 py-2.5 text-sm font-semibold text-foreground transition hover:border-accent hover:text-accent"
              >
                Run it locally
              </a>
            </div>
          </div>
        </section>

        {/* X Factor: Roast Engine */}
        <section id="roast" className="border-t border-border bg-surface-2/60">
          <div className="mx-auto w-full max-w-5xl px-6 py-20">
            <Badge>The X factor</Badge>
            <h2 className="mt-4 text-3xl font-semibold tracking-tight sm:text-4xl">
              Every month, LedgerLite roasts you.
            </h2>
            <p className="mt-4 max-w-2xl text-base leading-relaxed text-muted">
              At the end of each month, LedgerLite looks at your category
              breakdown — not a canned tip, an actual read on{" "}
              <em>your</em> numbers — and generates a one-liner verdict. It&apos;s
              procedural, not templated filler: the line changes based on
              which categories are out of proportion, which ones are at
              zero, and how far over cap you went.
            </p>

            <div className="mt-10 grid gap-4 sm:grid-cols-3">
              {roasts.map((r) => (
                <div
                  key={r.line}
                  className="flex flex-col justify-between rounded-xl border border-border bg-surface p-5 shadow-sm"
                >
                  <p className="text-[15px] leading-snug text-foreground">
                    &ldquo;{r.line}&rdquo;
                  </p>
                  <span className="mt-4 text-xs font-medium uppercase tracking-wide text-muted">
                    {r.tag}
                  </span>
                </div>
              ))}
            </div>

            <div className="mt-12 grid gap-8 sm:grid-cols-2">
              <div>
                <h3 className="text-sm font-semibold uppercase tracking-wide text-accent">
                  Per-category budget caps
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-muted">
                  Set a monthly cap on any category. Cross it, and the
                  dashboard doesn&apos;t wait for a report at month end — the row
                  turns red immediately, with the exact overage amount
                  displayed next to it, so you always know precisely how
                  far you went over and on what.
                </p>
              </div>
              <div>
                <h3 className="text-sm font-semibold uppercase tracking-wide text-accent">
                  Data-driven, not decorative
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-muted">
                  The roast generator runs entirely off your own ledger:
                  category ratios, zero-spend categories, and cap overages
                  feed a set of rules that pick the sharpest true statement
                  about your month — no LLM, no fluff, just your numbers
                  talking back.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* UI mockup */}
        <section className="border-t border-border">
          <div className="mx-auto w-full max-w-5xl px-6 py-20">
            <Badge>Dashboard</Badge>
            <h2 className="mt-4 text-3xl font-semibold tracking-tight sm:text-4xl">
              What you actually see.
            </h2>
            <p className="mt-4 max-w-2xl text-base leading-relaxed text-muted">
              A category-by-category breakdown with caps, overage badges,
              and the roast of the month sitting right at the top.
            </p>

            <div className="mt-10 overflow-hidden rounded-2xl border border-border bg-surface shadow-md">
              {/* mock window chrome */}
              <div className="flex items-center gap-1.5 border-b border-border bg-surface-2 px-4 py-3">
                <span className="h-2.5 w-2.5 rounded-full bg-danger/70" />
                <span className="h-2.5 w-2.5 rounded-full bg-accent-2/70" />
                <span className="h-2.5 w-2.5 rounded-full border border-border" />
                <span className="ml-3 text-xs text-muted font-mono-num">
                  localhost:5000/dashboard
                </span>
              </div>

              <div className="p-6 sm:p-8">
                {/* roast of the month callout */}
                <div className="rounded-xl border border-danger/30 bg-danger-bg px-5 py-4">
                  <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-danger">
                    <span>Roast of the month</span>
                  </div>
                  <p className="mt-1.5 text-[15px] font-medium text-foreground">
                    &ldquo;₹9,640 on food, ₹0 in savings. The fridge is fine.
                    The future isn&apos;t.&rdquo;
                  </p>
                </div>

                {/* category rows */}
                <div className="mt-6 divide-y divide-border overflow-hidden rounded-xl border border-border">
                  <div className="grid grid-cols-[1fr_auto_auto] gap-4 bg-surface-2 px-4 py-2.5 text-xs font-semibold uppercase tracking-wide text-muted">
                    <span>Category</span>
                    <span className="text-right">Spent / Cap</span>
                    <span className="text-right">Status</span>
                  </div>
                  {categories.map((c) => (
                    <div
                      key={c.name}
                      className={`grid grid-cols-[1fr_auto_auto] items-center gap-4 px-4 py-3 ${
                        c.over ? "bg-danger-bg" : "bg-surface"
                      }`}
                    >
                      <span
                        className={`text-sm font-medium ${
                          c.over ? "text-danger" : "text-foreground"
                        }`}
                      >
                        {c.name}
                      </span>
                      <span className="text-right text-sm font-mono-num text-muted">
                        {formatINR(c.spent)}{" "}
                        <span className="text-muted/70">
                          / {formatINR(c.cap)}
                        </span>
                      </span>
                      <span className="text-right">
                        {c.over ? (
                          <span className="inline-flex items-center rounded-full bg-danger px-2.5 py-1 text-xs font-semibold text-white">
                            +{formatINR(c.spent - c.cap)} over
                          </span>
                        ) : (
                          <span className="inline-flex items-center rounded-full border border-accent/40 px-2.5 py-1 text-xs font-medium text-accent">
                            on track
                          </span>
                        )}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Tech / concepts */}
        <section className="border-t border-border bg-surface-2/60">
          <div className="mx-auto w-full max-w-5xl px-6 py-16">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-muted">
              Built with
            </h2>
            <div className="mt-4 flex flex-wrap gap-2.5">
              {concepts.map((c) => (
                <Badge key={c}>{c}</Badge>
              ))}
            </div>
          </div>
        </section>

        {/* Run it */}
        <section id="run" className="border-t border-border">
          <div className="mx-auto w-full max-w-5xl px-6 py-20">
            <Badge>Get started</Badge>
            <h2 className="mt-4 text-3xl font-semibold tracking-tight sm:text-4xl">
              Run it locally
            </h2>
            <p className="mt-4 max-w-2xl text-base leading-relaxed text-muted">
              LedgerLite runs on Flask with PostgreSQL as the primary
              datastore. A SQLite fallback is available for local
              development if you don&apos;t want to stand up Postgres right
              away.
            </p>

            <div className="mt-8 overflow-hidden rounded-xl border border-border bg-[#0b0d0a] shadow-md">
              <div className="flex items-center gap-1.5 border-b border-white/10 px-4 py-2.5">
                <span className="h-2.5 w-2.5 rounded-full bg-danger/70" />
                <span className="h-2.5 w-2.5 rounded-full bg-accent-2/70" />
                <span className="h-2.5 w-2.5 rounded-full border border-white/20" />
                <span className="ml-2 text-xs text-white/50 font-mono-num">
                  shell
                </span>
              </div>
              <pre className="overflow-x-auto px-5 py-5 text-sm leading-relaxed text-[#d7ffe9] font-mono-num">
{`pip install -r requirements.txt

# PostgreSQL (recommended for full functionality)
export DATABASE_URL=postgresql://user:pass@localhost:5432/ledgerlite

# — or, for local dev without Postgres —
# omit DATABASE_URL to fall back to a local SQLite file

flask run
# → http://localhost:5000`}
              </pre>
            </div>

            <div className="mt-6 grid gap-4 text-sm text-muted sm:grid-cols-2">
              <div className="rounded-lg border border-border bg-surface p-4">
                <span className="font-semibold text-foreground">
                  PostgreSQL required for production
                </span>
                <p className="mt-1">
                  The app is built around Flask-SQLAlchemy against
                  PostgreSQL, configured via the{" "}
                  <code className="rounded bg-surface-2 px-1 py-0.5 font-mono-num text-xs">
                    DATABASE_URL
                  </code>{" "}
                  environment variable.
                </p>
              </div>
              <div className="rounded-lg border border-border bg-surface p-4">
                <span className="font-semibold text-foreground">
                  SQLite fallback for dev
                </span>
                <p className="mt-1">
                  Skip the Postgres setup while hacking locally — LedgerLite
                  falls back to SQLite so you can register, log in, and add
                  expenses immediately.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-border">
        <div className="mx-auto flex w-full max-w-5xl flex-col items-center justify-between gap-3 px-6 py-8 text-xs text-muted sm:flex-row">
          <span>LedgerLite · licensed under GPLv3</span>
          <a
            href="https://github.com"
            className="inline-flex items-center gap-1.5 hover:text-foreground"
          >
            <GitHubIcon className="h-3.5 w-3.5" />
            View source
          </a>
        </div>
      </footer>
    </div>
  );
}
