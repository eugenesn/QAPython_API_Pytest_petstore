from enum import Enum


class ErrorMessages(Enum):
    STATUS_CODE_NOT_EQUALS_OK = 'Status code not equals OK'
    STATUS_CODE_NOT_EQUALS_NOT_FOUND = 'Status code not equals NOT_FOUND'
    STATUS_CODE_NOT_EQUALS_INTERNAL_SERVER_ERROR = 'Status code not equals INTERNAL_SERVER_ERROR'
