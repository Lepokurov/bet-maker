from controllers.base import BaseController
from db.models import User
import uuid


class UserController(BaseController):
    model = User

    async def login(self, data):
        name = data.get("name")
        user = await self.get_one(filters={"name": name}, raise_not_exists_exception=False)
        if user:
            return user
        data["token"] = uuid.uuid4().hex
        user = await self.create(data=data)
        return user
