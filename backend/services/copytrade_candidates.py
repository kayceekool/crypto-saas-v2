def evaluate_trade(
    wallet_rank,
    token_score
):

    if (
        wallet_rank == "ELITE"
        and token_score >= 800
    ):

        return True

    if (
        wallet_rank == "SMART"
        and token_score >= 650
    ):

        return True

    return False