"""
Matan Zamir

main file
"""


import sys
import socket

from PyQt5.QtWidgets import QApplication
from clnt.GUI.GUIs.baseGUI import BaseGUI
from clnt.GUI.GUIs.window_names import WindowNames
from clnt.client_constants import EXIT
from clnt.recv_options import Recv
from clnt.server_ops import ServerOps


def main():
    """
    main, initiating gui
    """
    try:
        app = QApplication([])
        window = BaseGUI()
        window.window_call(WindowNames.LOGIN)
        window.client.socket.send(Recv.TEXT + ServerOps.CONNECT)
        sys.exit(app.exec())
    except socket.error as e:
        window.client.socket.close()
        print(e)
        sys.exit(EXIT)
    except Exception as e:
        print(e)
        sys.exit(EXIT)


if __name__ == '__main__':
    main()
