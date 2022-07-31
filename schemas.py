import decimal
import enum

from pydantic import BaseModel, Field


class BetState(enum.Enum):
    PENDING = "PENDING"
    FINISHED_WIN = "FINISHED_WIN"
    FINISHED_LOSE = "FINISHED_LOSE"


EventToBetState = {
    1: BetState.PENDING,
    2: BetState.FINISHED_WIN,
    3: BetState.FINISHED_LOSE,
}


class CreateBetModel(BaseModel):
    amount: decimal.Decimal = Field(description="amount amount")
    event_id: int = Field(description="event_id event_id")


class UserLoginModel(BaseModel):
    name: str = Field(description="login")


class UserModel(UserLoginModel):
    id: int
    token: str

    class Config:
        orm_mode = True


class EventStateModel(BaseModel):
    event_id: int
    state: int
