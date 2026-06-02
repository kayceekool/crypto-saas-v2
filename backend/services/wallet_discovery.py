discovered_wallets = set()


def add_wallet(
    wallet_address
):

    discovered_wallets.add(
        wallet_address
    )


def get_wallets():

    return list(
        discovered_wallets
    )