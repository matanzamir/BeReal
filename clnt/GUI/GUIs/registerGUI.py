"""
Matan Zamir

register gui window
"""


from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from clnt.GUI.GUIs.gui_inteface import GUIInterface
from clnt.GUI.GUIs.gui_protocol import GUIProtocol
from clnt.GUI.GUIs.window_names import WindowNames
from clnt.GUI.GUIs.gui_constants import *
from clnt.GUI.GUIs.register_requirements import *


class RegisterGUI(QMainWindow, GUIInterface):
    """
    register window class
    """
    def __init__(self, parent):
        """
        register window constructor
        """
        super().__init__(parent)
        uic.loadUi("GUI\\UIs\\signUpUI.ui", self)
        self.parent = parent
        self.signUpButton.clicked.connect(self.sign_up)
        self.loginSwitchButton.clicked.connect(self.login_gui)
        GUIProtocol.line_edit_validator(self.UsernameEnter)
        GUIProtocol.line_edit_validator(self.PasswordEnter)
        GUIProtocol.line_edit_validator(self.PasswordEnter_2)

    def sign_up(self):
        """
        sign up button event, checking entered information
        """
        username = self.UsernameEnter.text()
        password = self.PasswordEnter.text()
        password2 = self.PasswordEnter_2.text()
        if username is None or password is None or password2 is None:
            self.responseLabel.setText(ENTER_ALL)
        elif len(username) > LEN_OF_16:
            self.responseLabel.setText(UNDER_16)
        elif len(password) < LEN_OF_6:
            self.responseLabel.setText(ABOVE_6)
        elif password != password2:
            self.responseLabel.setText(MATCH)
        else:
            GUIProtocol.check(self, 'sign up')

    def login_gui(self):
        """
        login button event, calling login window
        """
        self.parent.window_call(WindowNames.LOGIN)
