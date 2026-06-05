from utils.constants import CURRENCIES


def get_minimum_reserve(bundles):

    if bundles < 10:
        return min(2, bundles)

    return max(1, round(bundles * 0.10))


def calculate_withdrawal(
    currency,
    requested_amount,
    warehouse
):

    tags = CURRENCIES[currency]

    result = []

    remaining = requested_amount

    available_data = []

    for tag in tags:

        notes = warehouse[currency][str(tag)]

        bundles = notes // 100

        reserve = get_minimum_reserve(
            bundles
        )

        usable = max(
            bundles - reserve,
            0
        )

        available_data.append(
            {
                "tag": tag,
                "notes": notes,
                "bundles": bundles,
                "reserve": reserve,
                "usable": usable,
                "bundle_value": tag * 100
            }
        )

    available_data.sort(
        key=lambda x: x["tag"],
        reverse=True
    )

    total_obtained = 0

    for item in available_data:

        tag = item["tag"]

        bundle_value = item["bundle_value"]

        usable = item["usable"]

        bundles_to_take = min(
            usable,
            remaining // bundle_value
        )

        value_taken = (
            bundles_to_take *
            bundle_value
        )

        notes_taken = (
            bundles_to_take *
            100
        )

        remaining -= value_taken

        total_obtained += value_taken

        result.append(
            {
                "tag": tag,
                "notes_taken": notes_taken,
                "bundles_taken": bundles_to_take,
                "value_taken": value_taken,
                "remaining_notes":
                    item["notes"] -
                    notes_taken,
                "remaining_bundles":
                    item["bundles"] -
                    bundles_to_take
            }
        )

    difference = (
        requested_amount -
        total_obtained
    )

    return {
        "currency": currency,
        "requested_amount":
            requested_amount,
        "obtained_amount":
            total_obtained,
        "difference":
            difference,
        "details":
            result
    }
