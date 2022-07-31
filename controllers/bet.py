from controllers.base import BaseController
from db.models import Bet


class BetController(BaseController):
    model = Bet

