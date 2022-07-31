from controllers.base import BaseController
from db.models import Bet


class BetController(BaseController):
    model = Bet

    async def update_bet_state(self, event_id, state):
        await self._update(model=self.model, filters={"event_id": event_id}, data={"state": state})
