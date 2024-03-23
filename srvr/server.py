"""
Matan Zamir

server
"""

import glob
import os
import socket
import sys
import time

from protocol import Protocol
import threading
from database.database_handler import DataBase
from recv_options import Recv
from operators import *
from server_methods import Methods
from server_constants import *


class Server:
    """
    server class
    """

    def __init__(self):
        """
        initiating server and database, listening to clients
        """
        try:
            self.db = DataBase(DB_PATH)
            self.delete_photos()
            self.heartbeat_mutex = threading.Lock()
            self.db_mutex = threading.Lock()
            bereal_thread = threading.Thread(target=self.timer)
            bereal_thread.start()
            self.server_socket = \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((IP, PORT))
            self.server_socket.listen(LISTEN)
        except socket.error as e:
            sys.exit(EXIT)

    def handle_clients(self):
        """
        handling clients that are connecting
        """
        while True:
            client_socket, address = self.server_socket.accept()
            socket_data = Protocol.receive(Recv.TEXT, client_socket).split()
            socket_type = socket_data[ARR_POS_0]
            if socket_type == 'receiving':
                client_id = socket_data[ARR_POS_1]
                CLIENTS_RECEIVING[client_id] = (client_socket, address)
            else:
                client_thread = threading.Thread(target=self.session,
                                                 args=(client_socket,))
                client_thread.start()

    def session(self, client_socket):
        """
        client session
        """
        try:
            name = ''
            param = ''
            while True:
                request = Protocol.receive(Recv.TEXT, client_socket)
                if SPLIT in request:
                    param, method_name = request.split(SPLIT)
                    if 'log out' in param:
                        Methods.ghost(self, name)
                        CLIENTS_RECEIVING[name] = None
                else:
                    method_name = request
                method = getattr(Methods, method_name)
                if method_name in NAME_PARAM_METHODS:
                    method(self, name, param)
                elif method_name in NAME_METHODS:
                    method(self, name)
                else:
                    name = method(self, client_socket)
        except socket.error as e:
            print(e)
            client_socket.close()

    def close(self):
        """
        closing the server
        """
        self.server_socket.close()
        sys.exit(EXIT)

    def timer(self):
        """
        timer thread. every BEREAL_TIME sends a bereal.
        """
        while True:
            time.sleep(BEREAL_TIME)
            self.delete_photos()
            getattr(Methods, 'be_real')(self)

    @staticmethod
    def delete_photos():
        """
        deleting database and photos
        """
        for file in glob.glob(f"{IMAGES_PATH}*"):
            os.remove(file)


def main():
    """
    main, initiating server
    """
    while True:
        try:
            server = Server()
            server.handle_clients()
        except socket.error as e:
            sys.exit(EXIT)


if __name__ == '__main__':
    main()
