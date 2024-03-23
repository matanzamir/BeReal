"""
Matan Zamir

server methods
"""
import os
import socket
import time

from server_constants import *
from recv_options import Recv
from operators import *
from server_responses import Resp
from srvr.protocol import Protocol


class Methods:
    @staticmethod
    def unfriend(server, user, friend):
        """
        removing relation from database
        """
        with server.db_mutex:
            server.db.remove_relation(user, friend)

    @staticmethod
    def add(server, user, friend):
        """
        adding a relation to database
        """
        with server.db_mutex:
            server.db.add_relation(user, friend)

    @staticmethod
    def ghost(server, name):
        """
        ghost function, sending ghost screen to clear receive
        """
        CLIENTS_RECEIVING[name][ARR_POS_0].send(Recv.GHOST)

    @staticmethod
    def create_list(friends, users):
        """
        creating list for users and friends
        """
        return PARAMS.join(friends) + SAP + PARAMS.join(users) + EOT

    @staticmethod
    def friends_filter(server, username, filter_str):
        friends_list, users_list = server.db.get_all_relations(username)
        friends_list = list(filter(
            lambda friend: filter_str.lower() in friend.lower(), friends_list))
        users_list = list(filter(
            lambda user: filter_str.lower() in user.lower(), users_list))
        encoded_list = Methods.create_list(friends_list, users_list).encode()
        CLIENTS_RECEIVING[username][ARR_POS_0].send(Recv.TEXT + encoded_list)

    @staticmethod
    def connect(server, client_socket: socket):
        """
        connects a not connected client to the server
        """
        approved = False
        response = ''
        username = ''
        while not approved:
            raw_request = Protocol.receive(Recv.TEXT, client_socket)
            action, username, password = raw_request.split(PARAMS, SPLIT_NUM)
            if action == 'login':
                response = Methods.manage_login(server, username, password)
            if action == 'sign up':
                response = Methods.manage_sign_up(server, username, password)
            if response == Resp.OK:
                approved = True
                if Methods.check_if_user_uploaded(username):
                    response += f' {Resp.SENT}'
            client_socket.send(Recv.TEXT + f'{response}{EOT}'.encode())
        return username

    @staticmethod
    def manage_login(server, username, password):
        """
        managing login request
        """
        if any(char in username for char in FORBIDDEN) or \
                any(char in password for char in FORBIDDEN):
            return Resp.SPECIAL
        elif server.db.check_if_user_exists(username):
            if username in CLIENTS_RECEIVING:
                if Methods.check_if_user_connected(server, username):
                    return Resp.CONNECTED
            if server.db.check_login(username, password):
                return Resp.OK
            else:
                return Resp.INCORRECT
        else:
            return Resp.NOT_EXIST

    @staticmethod
    def manage_sign_up(server, username, password):
        """
        managing sign up request
        """
        if not server.db.check_if_user_exists(username):
            server.db.add_user(username, password)
            return Resp.OK
        else:
            return Resp.EXIST

    @staticmethod
    def image(server, client_socket):
        """
        image handler
        """
        client_name, img_bytes = Protocol.receive(Recv.IMAGE, client_socket)
        Methods.save_image(server, img_bytes, client_name)
        Methods.send_image_to_friends(server, client_name)
        return client_name

    @staticmethod
    def save_image(server, img_bytes, client_name):
        """
        saving the client's image
        """
        with open(IMAGES_PATH + client_name + IMAGE_END, "wb") as photo_file:
            photo_file.write(img_bytes)

    @staticmethod
    def send_image_to_friends(server, username):
        """
        sending client's image to his friends
        """
        for friend in server.db.get_relations(username):
            if server.db.check_if_user_exists(friend) \
                    and Methods.check_if_user_uploaded(friend) \
                    and CLIENTS_RECEIVING[friend]:
                with server.heartbeat_mutex:
                    Protocol.send_image(CLIENTS_RECEIVING[friend][ARR_POS_0],
                                        Methods.get_image(username), username)

    @staticmethod
    def my_images(server, username):
        """
        sending the client his friends' pictures
        """
        for friend in server.db.get_relations(username):
            if server.db.check_if_user_exists(friend) and \
                    Methods.check_if_user_uploaded(friend):
                with server.heartbeat_mutex:
                    Protocol.send_image(CLIENTS_RECEIVING[username][ARR_POS_0],
                                        Methods.get_image(friend), friend)

    @staticmethod
    def check_if_user_uploaded(username):
        return os.path.isfile(IMAGES_PATH + username + IMAGE_END)

    @staticmethod
    def check_if_user_connected(server, username):
        """
        checking if a user is already connected
        """
        try:
            if not CLIENTS_RECEIVING[username]:
                return False
            with server.heartbeat_mutex:
                Methods.ghost(server, username)
                return True
        except socket.error:
            return False

    @staticmethod
    def get_image(client_name):
        """
        returning the client's image
        """
        with open(IMAGES_PATH + client_name + IMAGE_END, "rb") as photo_file:
            return photo_file.read()

    @staticmethod
    def be_real(server):
        """
        be real method. sends a bereal notification to all users
        """
        for user in server.db.get_all_users():
            if user in CLIENTS_RECEIVING and user:
                try:
                    CLIENTS_RECEIVING[user][ARR_POS_0].send(Recv.BEREAL)
                except socket.error as e:
                    print(e)
