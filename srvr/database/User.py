"""
Matan Zamir

users table
"""


from sqlalchemy import Column, String, Date, Integer
from srvr.database.base import Base


class User(Base):
    """
    user class
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        """
        user constructor
        """
        self.username = username
        self.password = password
