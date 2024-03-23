"""
Matan Zamir

protocol file
"""
from clnt.recv_options import Recv
from protocol_constants import *
from operators import *


class Protocol:

    @staticmethod
    def image(socket):
        """
        receiving image
        """
        bin_image = b''
        length = ''
        while len(length) != RECV_8:
            length += socket.recv(RECV_8 - len(length)).decode()
        if not length.isnumeric():
            return None, None
        else:
            length = int(length)
        name = ''
        while len(name) != RECV_16:
            name += socket.recv(RECV_16 - len(name)).decode()
        name = name.split(PARAMS)[ARR_POS_LAST]
        while length:
            chunk = socket.recv(CHUNK)
            bin_image += chunk
            length -= len(chunk)
            if length <= LEN_OF_0:
                return name, bin_image

    @staticmethod
    def words(socket):
        """
        receiving text
        """
        text = b''
        while True:
            chunk = socket.recv(RECV_6)
            if chunk[ARR_POS_LAST] == EOT_ASCII:
                text += chunk
                return text[:ARR_POS_LAST].decode()
            else:
                text += chunk

    @staticmethod
    def receive(wanted_action, socket):
        """
        general receiving function
        """
        while True:
            action = b''
            while len(action) != RECV_5:
                action += socket.recv(RECV_5 - len(action))
            if action == Recv.BEREAL:
                return Protocol.handle_bereal(wanted_action)
            if action == Recv.GHOST:
                return Protocol.handle_ghost(wanted_action)
            elif action == Recv.IMAGE:
                return Protocol.handle_image(wanted_action, socket)
            elif action == Recv.TEXT:
                return Protocol.handle_text(wanted_action, socket)

    @staticmethod
    def handle_text(wanted_action, socket):
        """
        handling received text
        """
        text = Protocol.words(socket)
        if wanted_action == Recv.TEXT:
            return text

    @staticmethod
    def handle_bereal(wanted_action):
        """
        handling received bereal
        """
        if wanted_action == Recv.IMAGE:
            return None, Recv.BEREAL
        else:
            return Recv.BEREAL

    @staticmethod
    def handle_image(wanted_action, socket):
        """
        handling received image
        """
        name, bin_image = Protocol.image(socket)
        if wanted_action == Recv.IMAGE:
            return name, bin_image
        elif wanted_action == Recv.GHOST:
            return

    @staticmethod
    def handle_ghost(wanted_action):
        """
        handling received ghost
        """
        if wanted_action == Recv.IMAGE:
            return None, None
        else:
            return

    @staticmethod
    def send_image(socket, bin_image, name):
        """
        sending an image
        """
        socket.send(Recv.IMAGE +
                    (str(len(bin_image)).zfill(LEN_OF_8)).encode() +
                    name.rjust(LEN_OF_16, PARAMS).encode() + bin_image)
