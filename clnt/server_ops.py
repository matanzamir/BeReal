"""
Matan Zamir

server operations enum
"""


from enum import Enum
from operators import *


class ServerOps(bytes, Enum):
    """
    server operations enum
    """
    CONNECT = f'connect{EOT}'.encode()
    IMAGE = f'image{EOT}'.encode()
    IMAGES = f'my_images{EOT}'.encode()
    GHOST = f'ghost{EOT}'.encode()
    SEARCH = f'friends_filter{EOT}'.encode()
