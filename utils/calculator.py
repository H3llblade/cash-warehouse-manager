from itertools import product
from utils.constants import CURRENCIES


def get_reserve(bundles):
    if bundles <= 5:
        return 1
    return max(1, round(bundles * 0.10))


def _proportional(requested_amount, data):
    """
    Distribuisce l'importo tra i tagli proporzionalmente alla loro
    capacità usabile (mazzette × valore mazzetta).

    Fase 1 — quota proporzionale (floor): ogni taglio riceve una
    fetta di mazzette commisurata alla propria capacità.
    Fase 2 — residuo con greedy: il valore rimasto viene assegnato
    partendo dal taglio più grande.

    Restituisce (combo_list, remaining).
    """
    total_capacity = sum(
        item["usable"] * item["bundle_value"]
        for item in data
        if item["usable"] > 0
    )
    if total_capacity == 0:
        return [0] * len(data), requested_amount

    result    = [0] * len(data)
    remaining = requested_amount

    # Fase 1: quota proporzionale
    for i, item in enumerate(data):
        if item["usable"] == 0:
            continue
        share   = (item["usable"] * item["bundle_value"]) / total_capacity
        target  = share * requested_amount
        bundles = min(item["usable"], int(target // item["bundle_value"]))
        result[i]  = bundles
        remaining -= bundles * item["bundle_value"]

    # Fase 2: residuo (greedy dal taglio più grande)
    for i, item in enumerate(data):
        if remaining <= 0:
            break
        available = item["usable"] - result[i]
        if available > 0 and remaining >= item["bundle_value"]:
            extra       = min(available, remaining // item["bundle_value"])
            result[i]  += extra
            remaining  -= extra * item["bundle_value"]

    return result, remaining


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

    # ── Strategia 1: distribuzione proporzionale ─────────────────────
    # Usa tutti i tagli disponibili in proporzione alla loro capacità.
    prop_list, prop_remaining = _proportional(requested_amount, data)

    if prop_remaining == 0:
        best_combo = tuple(prop_list)

    else:
        # ── Strategia 2: ricerca esaustiva (fallback) ─────────────────
        # Necessaria quando i tagli non sono multipli esatti tra loro
        # (es. EUR 100/50/20 → mazzette 10000/5000/2000).
        prop_total      = requested_amount - prop_remaining
        best_combo      = tuple(prop_list)
        best_difference = abs(prop_remaining)
        best_total      = prop_total

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
