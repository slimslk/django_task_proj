from rest_framework import status

from task_app.constants.exception_message_constants import (
    NO_CONTENT_EXCEPTION_DATA, NOTHING_TO_UPDATE_MSG, NOTHING_TO_UPDATE_DATA,
)


class TaskAppBaseException(Exception):
    def __init__(self, message: str, data: str | dict | list, status_code: int):
        self.message = message
        self.status_code = status_code
        self.data = data
        super().__init__(message)
        

class NoContentException(TaskAppBaseException):
    def __init__(self):
        msg = "CONTENT NOT FOUND"
        super().__init__(msg, **NO_CONTENT_EXCEPTION_DATA)


class BadRequestException(TaskAppBaseException):
    def __init__(self, message: str | dict):
        self.msg = message
        super().__init__(message=self.msg, data=self.msg, status_code=status.HTTP_400_BAD_REQUEST)


class CreateValidationError(TaskAppBaseException):
    def __init__(self, message: str | dict):
        super().__init__(message=message, data=message, status_code=status.HTTP_400_BAD_REQUEST)


class NothingToUpdateException(TaskAppBaseException):
    def __init__(self):
        self.msg = NOTHING_TO_UPDATE_MSG
        super().__init__(message=self.msg, **NOTHING_TO_UPDATE_DATA)
