"""
Matan Zamir

window names Enum
"""


from enum import Enum


class WindowNames(str, Enum):
    """
    window names enum
    """
    LOGIN = 'LOGIN'
    REGISTER = 'REGISTER'
    CAMERA = 'CAMERA'
    MAIN = 'MAIN'
    FRIENDS = 'FRIENDS'
    SEARCH = 'SEARCH'
