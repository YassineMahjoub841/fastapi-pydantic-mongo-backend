"""UTILS
Misc helpers/utils functions
"""

# # Native # #
from time import time
from uuid import uuid4
from typing import Union
from pydantic_core import PydanticCustomError
from typing import  Union, TypeVar

__all__ = ("get_time", "get_uuid", "validate_unique_list")


def get_time(seconds_precision=True) -> Union[int, float]:
    """Returns the current time as Unix/Epoch timestamp, seconds precision by default"""
    return time() if not seconds_precision else int(time())


def get_uuid() -> str:
    """Returns an unique UUID (UUID4)"""
    return str(uuid4())

T = TypeVar("T")
def validate_unique_list(v: list[T]) -> list[T]:
    """
    Validates that the input list contains unique elements and raises an exception if it doesn't. 
    Args:
        v: A list of type T to be validated for uniqueness.
    Returns:
        The input list v if it contains unique elements.
    Raises:
        PydanticCustomError: If the input list v contains duplicate elements.
    """
    print(len(v), len(set(v)))
    if len(v) != len(set(v)):
        raise PydanticCustomError('unique_list', 'List must be unique')
    return v