from enum import Enum

class Types:
    class Connection(Enum):
        FROM_TYPE_DB = 0
        FROM_TYPE_CSV = 1
        _READ_ID_LIST = 101