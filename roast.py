"""
Procedural "spending roast" generator.

Given this month's spend-by-category and the user's budget caps, this module
picks the most relevant roast template from several distinct patterns and
fills it in with real numbers computed from the data. It is intentionally
*not* a single static string -- different data shapes trigger different
templates, gated on actual ratios/overages/near-zero conditions.
"""

import random
from decimal import Decimal

# Categories that are "fun" / discretionary vs. "responsible" -- used to spot
# funny ratio pairs (e.g. Food vs Rent, Entertainment vs Savings).
DISCRETIONARY = {"Food", "Entertainment", "Subscriptions", "Shopping"}
RESPONSIBLE = {"Savings", "Rent", "Utilities", "Health"}

NO_DATA_LINES = [
    "No expenses logged this month. Either you're broke, rich, or lying.",
    "Zero expenses this month. Suspiciously well-behaved. We're watching.",
]


def _fmt(amount) -> str:
    amount = Decimal(amount)
    return f"₹{amount:,.2f}"


def _pct(part, whole) -> int:
    if whole == 0:
        return 0
    return int(round((Decimal(part) / Decimal(whole)) * 100))


def generate_roast(spend_by_category: dict, budgets_by_category: dict) -> str:
    """
    spend_by_category: {category: Decimal(total spent this month)}
    budgets_by_category: {category: Decimal(monthly cap)}  (only categories
        with a cap set need to be present)

    Returns a single roast line, procedurally selected and filled in.
    """
    spend = {k: Decimal(v) for k, v in spend_by_category.items() if Decimal(v) > 0}

    if not spend:
        return random.choice(NO_DATA_LINES)

    total = sum(spend.values())

    # --- Pattern 1: a category is badly over its budget cap -----------------
    worst_overage = None  # (category, over_amount, pct_over)
    for cat, cap in budgets_by_category.items():
        cap = Decimal(cap)
        spent = spend.get(cat, Decimal("0"))
        if cap > 0 and spent > cap:
            over_amount = spent - cap
            pct_over = _pct(over_amount, cap)
            if worst_overage is None or over_amount > worst_overage[1]:
                worst_overage = (cat, over_amount, pct_over)

    if worst_overage and worst_overage[2] >= 50:
        cat, over_amount, pct_over = worst_overage
        templates = [
            f"You blew past your {cat} budget by {_fmt(over_amount)} ({pct_over}% over cap). Bold move.",
            f"{cat} cap? What {cat} cap. You're {_fmt(over_amount)} over ({pct_over}%).",
        ]
        return random.choice(templates)

    # --- Pattern 2: near-zero on a "responsible" category, real money on a
    # discretionary one -----------------------------------------------------
    zero_responsible = [c for c in RESPONSIBLE if spend.get(c, Decimal("0")) == 0]
    big_discretionary = [
        (c, amt) for c, amt in spend.items()
        if c in DISCRETIONARY and amt >= (total * Decimal("0.15"))
    ]
    if zero_responsible and big_discretionary:
        zero_cat = zero_responsible[0]
        disc_cat, disc_amt = max(big_discretionary, key=lambda x: x[1])
        templates = [
            f"₹0 on {zero_cat}, {_fmt(disc_amt)} on {disc_cat} -- bold strategy.",
            f"You put nothing toward {zero_cat} but found {_fmt(disc_amt)} for {disc_cat}. Priorities?",
        ]
        return random.choice(templates)

    # --- Pattern 3: one category dwarfs another by a large ratio -----------
    best_ratio_pair = None  # (bigger_cat, smaller_cat, ratio)
    cats = list(spend.items())
    for big_cat, big_amt in cats:
        for small_cat, small_amt in cats:
            if big_cat == small_cat:
                continue
            if small_amt <= 0:
                continue
            ratio = big_amt / small_amt
            if ratio >= 3 and big_amt >= (total * Decimal("0.1")):
                if best_ratio_pair is None or ratio > best_ratio_pair[2]:
                    best_ratio_pair = (big_cat, small_cat, ratio)

    if best_ratio_pair:
        big_cat, small_cat, ratio = best_ratio_pair
        ratio_display = int(ratio) if ratio == int(ratio) else round(float(ratio), 1)
        templates = [
            f"You spent {ratio_display}x more on {big_cat} than {small_cat}. Priorities?",
            f"{big_cat} is beating {small_cat} {ratio_display}-to-1 this month. Interesting choice.",
        ]
        return random.choice(templates)

    # --- Pattern 4: one category dominates total spend ----------------------
    top_cat, top_amt = max(spend.items(), key=lambda x: x[1])
    top_share = _pct(top_amt, total)
    if top_share >= 50:
        templates = [
            f"{top_cat} alone ate {top_share}% of your entire month ({_fmt(top_amt)} of {_fmt(total)}). Everything else is a rounding error.",
            f"{top_share}% of your money this month went to {top_cat}. At this point it's basically a subscription to your own life.",
        ]
        return random.choice(templates)

    # --- Pattern 5: mild overage (some category over cap but < 50%) --------
    if worst_overage:
        cat, over_amount, pct_over = worst_overage
        return f"You're {_fmt(over_amount)} over your {cat} budget this month ({pct_over}% over). Not great, not catastrophic."

    # --- Fallback: no dramatic pattern found, still say something real -----
    templates = [
        f"Your biggest expense this month was {top_cat} at {_fmt(top_amt)} ({top_share}% of {_fmt(total)}). Make of that what you will.",
        f"Total spend this month: {_fmt(total)}, mostly on {top_cat}. Living deliberately, or just living.",
    ]
    return random.choice(templates)
