from core.config import (
    WHALE_THRESHOLD
)


class WhaleDetector:

    @staticmethod
    def detect(amount):

        if amount >= 100000:

            return "MEGA_WHALE"

        if amount >= 25000:

            return "WHALE"

        if amount >= WHALE_THRESHOLD:

            return "SHARK"

        return None