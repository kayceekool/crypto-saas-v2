def calculate_winrate(
    wins,
    losses
):

    total = wins + losses

    if total == 0:

        return 0

    return round(
        (wins / total) * 100,
        2
    )