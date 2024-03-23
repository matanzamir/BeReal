"""
Matan Zamir

recv options enum
"""


from enum import Enum


class Recv(bytes, Enum):
    """
    recv options enum
    """
    IMAGE = 'image'.encode()
    TEXT = 'words'.encode()
    GHOST = 'ghost'.encode()
    BEREAL = 'BReal'.encode()
