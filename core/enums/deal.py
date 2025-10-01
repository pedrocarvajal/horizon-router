from enum import IntEnum


class DealTypes(IntEnum):
    ORDER_TYPE_BUY = 0
    ORDER_TYPE_SELL = 1


class DealDirections(IntEnum):
    IN = 0
    OUT = 1
