from models.alert import (
    Alert
)


class AlertRepository:

    @staticmethod
    async def save_alert(
        db,
        level,
        title,
        message
    ):

        alert = Alert(
            level=level,
            title=title,
            message=message
        )

        db.add(
            alert
        )

        await db.commit()

        return alert