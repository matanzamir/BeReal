"""
Matan Zamir

base gui window
"""
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from clnt.client import Client
from clnt.GUI.GUIs.windows_mapping import WINDOWS_MAPPING


class BaseGUI(QMainWindow):
    """
    base window class
    """
    def __init__(self):
        """
        constructor of the window
        """
        super(BaseGUI, self).__init__()
        uic.loadUi("GUI\\UIs\\baseUI.ui", self)
        self.client = Client()
        self.window = None

    def window_call(self, window_name):
        """
        closes the previous window and creates a new window
        """
        window_class = WINDOWS_MAPPING[window_name]
        if self.window:
            self.window.stop()
            self.window.close()
        self.window = window_class(self)
        self.window.start()
        self.window.show()
