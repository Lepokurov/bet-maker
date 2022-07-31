from sqlalchemy import Column, Enum, ForeignKey, DECIMAL
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from db.models.base import BaseSQLModel
from schemas import BetState


class Bet(BaseSQLModel):
    __tablename__ = "bet"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False)
    amount = Column(DECIMAL, nullable=False, gt=0)
    state = Column(Enum(BetState), default=BetState.NEW.value)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    users = relationship("User", lazy="noload", back_populates="bets")
