from itertools import product
from utils.constants import CURRENCIES


def get_reserve(bundles):
    if bundles <= 5:
        return 1
    return max(1, round(bundles * 0.10))


def calculate_withdrawal(currency, requested_amount, warehouse):
    tags = CURRENCIES[currency]

    data = []
    for tag in tags:
        notes   = int(warehouse[currency][str(tag)])
        bundles = notes // 100
        reserve = get_reserve(bundles)
        usable  = max(0, bundles - reserve)
        data.append({
            "tag":          tag,
            "notes":        notes,
            "bundles":      bundles,
            "usable":       usable,
            "bundle_value": tag * 100,
        })

    # ── Step 1: greedy (taglio più grande → più piccolo) ─────────────
    # Usa quante mazzette possibili del taglio maggiore, poi scende.
    # Questo produce la combinazione con il minor numero di mazzette
    # e privilegia i tagli alti.
    greedy = []
    remaining = requested_amount
    for item in data:
        taken = (
            min(item["usable"], remaining // item["bundle_value"])
            if remaining >= item["bundle_value"]
            else 0
        )
        greedy.append(taken)
        remaining -= taken * item["bundle_value"]

    if remaining == 0:
        # Match esatto trovato con greedy: usato direttamente
        best_combo = tuple(greedy)
    else:
        # ── Step 2: ricerca esaustiva (fallback) ──────────────────────
        # Necessaria quando i tagli non sono multipli esatti tra loro
        # (es. EUR 100/50/20 → mazzette 10000/5000/2000).
        # Inizia dall'esito greedy come baseline.
        best_combo      = tuple(greedy)
        best_difference = abs(remaining)
        best_total      = requested_amount - remaining

        ranges = [range(item["usable"] + 1) for item in data]

        for combo in product(*ranges):
            total      = sum(b * data[i]["bundle_value"] for i, b in enumerate(combo))
            difference = abs(requested_amount - total)

            if difference < best_difference or (
                difference == best_difference and total > best_total
            ):
                best_difference = difference
                best_combo      = combo
                best_total      = total

                if difference == 0:
                    break

    # ── Costruzione risultato ────────────────────────────────────────
    result   = []
    obtained = 0

    for i, bundles_taken in enumerate(best_combo):
        value_taken = bundles_taken * data[i]["bundle_value"]
        obtained   += value_taken
        result.append({
            "tag":               data[i]["tag"],
            "bundles_taken":     bundles_taken,
            "notes_taken":       bundles_taken * 100,
            "value_taken":       value_taken,
            "remaining_notes":   data[i]["notes"] - bundles_taken * 100,
            "remaining_bundles": data[i]["bundles"] - bundles_taken,
        })

    return {
        "currency":         currency,
        "requested_amount": requested_amount,
        "obtained_amount":  obtained,
        "difference":       obtained - requested_amount,
        "details":          result,
    }
