from enum import Enum

class Status(Enum):
    ADD_INIT = 0
    ADD_IN_PROGRESS = 1
    ADD_DONE = 2
    UPDATE = 3
    ACTIVE = 4
    REMOVE = 5

class FolderObjectType(Enum):
    FOLDER = 0
    FILE = 1

class Constants(Enum):
    OK = 0
    EROOR = 1
    NOT_COMPLETE = 2
    NOT_EXIST = 3
    DEFAULT = 4