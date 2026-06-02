class AlertEngine:

    @staticmethod
    def should_alert(token):

        if token["score"] >= 800:
            return True

        return False