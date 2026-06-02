tracked_wallets = {}

def update_wallet(
    wallet,
    pnl
):

    if wallet not in tracked_wallets:

        tracked_wallets[wallet] = {
            "wins": 0,
            "losses": 0
        }

    if pnl > 0:

        tracked_wallets[wallet]["wins"] += 1

    else:

        tracked_wallets[wallet]["losses"] += 1