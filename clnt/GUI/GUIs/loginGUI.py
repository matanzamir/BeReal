"""
Matan Zamir

login gui screen
"""


from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

from clnt.GUI.GUIs.gui_inteface import GUIInterface
from clnt.GUI.GUIs.window_names import WindowNames
from functools import partial
from clnt.GUI.GUIs.gui_protocol import GUIProtocol


class LoginGUI(QMainWindow, GUIInterface):
    """
    login gui class
    """

    def __init__(self, parent):
        """
        constructor for login window
        """
        super().__init__(parent)
        uic.loadUi("GUI\\UIs\\loginUI.ui", self)
        self.parent = parent
        self.LoginButton.clicked.connect(partial(GUIProtocol.check,
                                                 obj=self, action='login'))
        self.signUpSwitchButton.clicked.connect(self.sign_up_gui)
        GUIProtocol.line_edit_validator(self.UsernameEnter)
        GUIProtocol.line_edit_validator(self.PasswordEnter)

    def sign_up_gui(self):
        """
        sign up button event, calling sign up screen
        """
        self.parent.window_call(WindowNames.REGISTER)
