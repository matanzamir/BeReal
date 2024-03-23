"""
Matan Zamir

client initiator
"""


import socket

from PyQt5.QtWidgets import QMessageBox

import protocol
from recv_options import Recv
from operators import *
from client_constants import *


class Client:
    """
    client class
    """
    def __init__(self):
        """
        client constructor
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((IP, PORT))
            self.socket.send(Recv.TEXT + f'sending{EOT}'.encode())
            self.username = None
            self.listen_socket = None
        except socket.error as e:
            print(e)

    def connected(self):
        """
        initiating receiving socket
        """
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.connect((IP, PORT))
        encoded_socket_type = f'receiving {self.username}{EOT}'.encode()
        self.listen_socket.send(Recv.TEXT + encoded_socket_type)

    def connect_check(self, action, username, password):
        """
        checking if approved, if so, connecting
        """
        request = action + PARAMS + username + PARAMS + password + EOT
        self.socket.send(Recv.TEXT + request.encode())
        response = protocol.Protocol.receive(Recv.TEXT, self.socket)
        if 'approved' in response:
            self.username = username
            self.connected()
        return response
