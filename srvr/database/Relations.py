"""
Matan Zamir

relations table
"""


from sqlalchemy import Column, Integer, ForeignKey
from srvr.database.base import Base


class Relation(Base):
    """
    relations class
    """

    __tablename__ = 'relations'

    username = Column(Integer, ForeignKey('users.id'),
                      primary_key=True, nullable=False)
    friend = Column(Integer, ForeignKey('users.id'),
                    primary_key=True, nullable=False)

    def __init__(self, username, friend):
        """
        relation constructor
        """
        self.username = username
        self.friend = friend
