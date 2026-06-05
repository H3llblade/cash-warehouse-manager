from itertools import product
from utils.constants import CURRENCIES


def get_reserve(bundles):

    if bundles <= 5:
        return 1

    return max(
        1,
        round(bundles * 0.10)
    )


def calculate_withdrawal(
    currency,
    requested_amount,
    warehouse
):

    tags = CURRENCIES[currency]

    data = []

    for tag in tags:

        notes = int(
            warehouse[currency][str(tag)]
        )

        bundles = notes // 100

        reserve = get_reserve(
            bundles
        )

        usable = max(
            0,
            bundles - reserve
        )

        data.append(
            {
                "tag": tag,
                "notes": notes,
                "bundles": bundles,
                "usable": usable,
                "bundle_value": tag * 100
            }
        )

    ranges = [
        range(item["usable"] + 1)
        for item in data
    ]

    best_combo = None
    best_difference = None
    best_total = None

    for combo in product(*ranges):

        total = 0

        for i, bundles_taken in enumerate(combo):

            total += (
                bundles_taken *
                data[i]["bundle_value"]
            )

        difference = abs(
            requested_amount - total
        )

        # A parità di differenza preferisce la combo che dà più denaro
        # (evita di restituire 0 quando esiste una soluzione parziale)
        better = (
            best_difference is None
            or difference < best_difference
            or (
                difference == best_difference
                and total > best_total
            )
        )

        if better:

            best_difference = difference
            best_combo = combo
            best_total = total

            if difference == 0:
                break

    result = []

    obtained = 0

    for i, bundles_taken in enumerate(best_combo):

        value_taken = (
            bundles_taken *
            data[i]["bundle_value"]
        )

        obtained += value_taken

        result.append(
            {
                "tag":
                    data[i]["tag"],

                "bundles_taken":
                    bundles_taken,

                "notes_taken":
                    bundles_taken * 100,

                "value_taken":
                    value_taken,

                "remaining_notes":
                    data[i]["notes"]
                    -
                    (
                        bundles_taken
                        * 100
                    ),

                "remaining_bundles":
                    data[i]["bundles"]
                    -
                    bundles_taken
            }
        )

    return {
        "currency":
            currency,

        "requested_amount":
            requested_amount,

        "obtained_amount":
            obtained,

        "difference":
            obtained
            -
            requested_amount,

        "details":
            result
    }
