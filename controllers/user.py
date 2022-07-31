from controllers.base import BaseController
from db.models import User


class BetController(BaseController):
    model = User

