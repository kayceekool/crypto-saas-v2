class WhaleDetector:

    @staticmethod
    def detect(trade_size):

        if trade_size >= 100000:
            return "MEGA_WHALE"

        if trade_size >= 25000:
            return "WHALE"

        if trade_size >= 5000:
            return "SHARK"

        return "RETAIL"