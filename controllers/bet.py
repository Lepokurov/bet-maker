from controllers.base import BaseController
from db.models import Bet


class BetController(BaseController):
    model = Bet

    async def update_bet_state(self, event_status_data):
        event_id = event_status_data.get("event_id")
        state = event_status_data.get("state")
        await self._update(model=self.model, filters={"event_id": event_id}, data={"state": state})
