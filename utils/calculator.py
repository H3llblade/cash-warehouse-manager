from itertools import product
from utils.constants import CURRENCIES


def get_reserve(bundles):
    if bundles < 10:
        return min(2, bundles)

    return max(2, round(bundles * 0.10))


def calculate_withdrawal(
    currency,
    requested_amount,
    warehouse
):

    tags = CURRENCIES[currency]

    data = []

    for tag in tags:

        notes = warehouse[currency][str(tag)]

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
                "bundles": bundles,
                "usable": usable,
                "bundle_value": tag * 100,
                "notes": notes
            }
        )

    ranges = [
        range(item["usable"] + 1)
        for item in data
    ]

    best_solution = None
    best_score = -999999999

    for combo in product(*ranges):

        total = 0

        used_tags = 0

        for i, amount in enumerate(combo):

            total += (
                amount *
                data[i]["bundle_value"]
            )

            if amount > 0:
                used_tags += 1

        difference = abs(
            requested_amount - total
        )

        residual_stock = 0

        imbalance = 0

        percentages = []

        for i, amount in enumerate(combo):

            residual_stock += (
                data[i]["usable"] -
                amount
            )

            if data[i]["usable"] > 0:

                percentages.append(
                    amount /
                    data[i]["usable"]
                )

        if len(percentages) > 1:

            imbalance = (
                max(percentages)
                -
                min(percentages)
            )

        score = 0

        score -= difference

        score += (
            used_tags * 100000
        )

        score += (
            residual_stock * 10
        )

        score -= (
            imbalance * 1000
        )

        if score > best_score:

            best_score = score

            best_solution = combo

    result = []

    obtained = 0

    for i, bundles_taken in enumerate(
        best_solution
    ):

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
                        *
                        100
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
            obtained -
            requested_amount,

        "details":
            result
    }
