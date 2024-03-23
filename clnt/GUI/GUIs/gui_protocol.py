"""
Matan Zamir

gui protocol
"""
import socket

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMessageBox

from clnt.GUI.GUIs.window_names import WindowNames
from clnt.GUI.GUIs.gui_constants import *
from clnt.server_responses import Resp


class GUIProtocol:
    @staticmethod
    def check(obj, action):
        """
        checking server's response
        """
        try:
            response = \
                obj.parent.client.connect_check(action,
                                                obj.UsernameEnter.text(),
                                                obj.PasswordEnter.text())
            if Resp.OK in response:
                if Resp.SENT in response:
                    obj.parent.window_call(WindowNames.MAIN)
                else:
                    obj.parent.window_call(WindowNames.CAMERA)
            else:
                obj.responseLabel.setText(response)
        except socket.error as e:
            obj.parent.client.socket.close()
            print(e)
            QMessageBox.about(obj, ERROR_TITLE, CONNECT_ERROR + action)
        except Exception as e:
            print(e)

    @staticmethod
    def line_edit_validator(line_edit):
        """
        validating text integrity
        """
        regex = QRegExp("[a-zA-Z0-9]*")
        validator = QRegExpValidator(regex)
        line_edit.setValidator(validator)
