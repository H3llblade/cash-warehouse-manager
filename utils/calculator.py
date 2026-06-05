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

    tags = sorted(
        CURRENCIES[currency],
        reverse=True
    )

    available = []

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

        available.append(
            {
                "tag": tag,
                "bundles": bundles,
                "usable": usable,
                "notes": notes,
                "bundle_value": tag * 100
            }
        )

    remaining = requested_amount

    result = []

    obtained = 0

    for item in available:

        tag = item["tag"]

        bundle_value = item["bundle_value"]

        usable = item["usable"]

        bundles_taken = min(
            usable,
            remaining // bundle_value
        )

        value_taken = (
            bundles_taken *
            bundle_value
        )

        obtained += value_taken

        remaining -= value_taken

        result.append(
            {
                "tag": tag,
                "bundles_taken": bundles_taken,
                "notes_taken": bundles_taken * 100,
                "value_taken": value_taken,
                "remaining_notes":
                    item["notes"]
                    -
                    (
                        bundles_taken
                        * 100
                    ),
                "remaining_bundles":
                    item["bundles"]
                    -
                    bundles_taken
            }
        )

    difference = (
        obtained
        -
        requested_amount
    )

    return {
        "currency":
            currency,

        "requested_amount":
            requested_amount,

        "obtained_amount":
            obtained,

        "difference":
            difference,

        "details":
            result
    }
