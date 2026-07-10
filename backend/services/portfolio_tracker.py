class PortfolioTracker:

    positions = {}

    @classmethod
    def open_position(

        cls,

        wallet,

        token,

        price

    ):

        cls.positions[
            (
                wallet,
                token
            )
        ] = {

            "entry":
                price,

            "status":
                "OPEN"
        }

    @classmethod
    def close_position(

        cls,

        wallet,

        token,

        price

    ):

        position = cls.positions.get(

            (
                wallet,
                token
            )

        )

        if not position:

            return None

        pnl = (

            price -

            position["entry"]

        )

        position["status"] = "CLOSED"

        position["exit"] = price

        position["pnl"] = pnl

        return pnl