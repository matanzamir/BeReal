"""
Matan Zamir

server responses enum
"""

from enum import Enum


class Resp(str, Enum):
    OK = 'approved'
    INCORRECT = 'password or username are incorrect'
    NOT_EXIST = 'user does not exist'
    EXIST = 'username already exists'
    CONNECTED = 'user already connected'
    SPECIAL = "username and password can't " \
              "contain any special character and or spacer"
    SENT = 'sent'
