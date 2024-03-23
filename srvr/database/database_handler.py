"""
Matan Zamir

database class and handler
"""
import hashlib
import os
from datetime import date
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from srvr.database.Relations import Relation
from srvr.database.User import User
from srvr.database.base import Base
from srvr.database.db_constants import *


class DataBase:
    def __init__(self, path):
        """
        database constructor, initiating database
        """
        engine = create_engine(f"sqlite:///{path}")
        Base.metadata.bind = engine
        inspector = inspect(engine)
        if not inspector.has_table("db"):
            Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def check_if_user_exists(self, username: str):
        """
        checks if a user with the same username already exists
        """
        return len(self.session.query(User).filter(
            User.username == username).all()) > LEN_OF_0

    def add_user(self, username, password):
        """
        adding a user to the database
        """
        self.session.add(User(username, self.hash(password)))
        self.session.commit()

    @staticmethod
    def hash(password):
        """
        hashing the password
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def check_login(self, username: str, password):
        """
        checking if the login failed or succeeded
        """
        return self.session.query(User.password).filter(
            User.username == username).first()[ARR_POS_0] == self.hash(password)

    def get_all_usernames(self):
        """
        getting all the usernames in the database
        """
        raw_list = self.session.query(User.username).all()
        users_list = []
        for user in raw_list:
            users_list.append(user[ARR_POS_0])
        return users_list

    def add_relation(self, username, friend):
        """
        adding a relation between two users
        """
        try:
            self.session.add(Relation(self.get_id(username),
                                      self.get_id(friend)))
            self.session.add(Relation(self.get_id(friend),
                                      self.get_id(username)))
            self.session.commit()
        except exc.IntegrityError:
            print('relation already exists')

    def remove_relation(self, username, friend):
        """
        removing a relationship from the database
        """
        try:
            self.session.query(Relation).filter_by(
                username=self.get_id(username),
                friend=self.get_id(friend)).delete()
            self.session.query(Relation).filter_by(
                username=self.get_id(friend),
                friend=self.get_id(username)).delete()
            self.session.commit()
        except exc.IntegrityError:
            print('relation does not exist')

    def get_relations(self, username: str):
        """
        getting all the relations of a user
        """
        raw_friends_list = self.session.query(Relation.friend).filter(
            Relation.username == self.get_id(username)).all()
        friends_list = []
        for friend in raw_friends_list:
            friends_list.append(self.get_user(friend[ARR_POS_0]))
        return friends_list

    def get_all_relations(self, username: str):
        """
        getting all the relations of a user
        """
        friends_list = self.get_relations(username)
        users_list = self.session.query(User.username).filter(
            User.username != username).all()
        users_list = list(map(lambda user: user[ARR_POS_0], users_list))
        updated_users_list = []
        for user in users_list:
            if user not in friends_list:
                updated_users_list.append(user)
        return friends_list, updated_users_list

    def get_id(self, username: str) -> int:
        """
        getting user's id by name
        """
        return self.session.query(User.id).filter(
            User.username == username).first()[ARR_POS_0]

    def get_user(self, id: int):
        """
        getting user's name by id
        """
        return self.session.query(User.username).filter(
            User.id == id).first()[ARR_POS_0]

    def get_all_users(self):
        """
        getting all users names
        """
        users_list = self.session.query(User.username).all()
        return list(map(lambda user: user[ARR_POS_0], users_list))
