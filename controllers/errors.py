from fastapi import Request, Response
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from starlette.responses import JSONResponse

ForeignKeyViolationErrorCode = '23503'


class BaseControllerException(SQLAlchemyError):
    def __init__(self, model):
        self._model = str(model.__table__)

    def message(self):
        return f"Model: {self._model}"


class ObjectDoestExistControllerException(BaseControllerException):
    def __init__(self, model, filters):
        self._model = str(model.__table__)
        self._filters = filters

    def message(self):
        return f"{self._model} with filters {self._filters} doesn't exists"


class NotAllowedActionControllerException(BaseControllerException):
    def __init__(self, reason: str):
        self._reason = reason

    def message(self):
        return f"Action not allowed. {self._reason}"


class BadRequestControllerException(BaseControllerException):
    def __init__(self, reason: str):
        self._reason = reason

    def message(self):
        return f"Not correct format. {self._reason}"


def sql_alchemy_error_message_formatter(err: SQLAlchemyError):
    raw_message = str(err).split('DETAIL: ')
    if len(raw_message) < 1:
        return raw_message[0]
    message = raw_message[1]
    if message.startswith(' '):
        message = message[1:]
    if '"' in message:
        message = message.replace('"', "'")
    return message


async def controller_exceptions_handler(request: Request, exc: SQLAlchemyError):
    match exc:
        case ObjectDoestExistControllerException() as err:
            return JSONResponse(status_code=400, content={"message": err.message()})
        case NotAllowedActionControllerException() as err:
            return JSONResponse(status_code=403, content={"message": err.message()})
        case SQLAlchemyError() as err:
            error_message = sql_alchemy_error_message_formatter(err.args[0])
            return JSONResponse(status_code=500, content={"error": error_message})
