"""
Matan Zamir

windows mapping dictionary
"""


from PyQt5.QtWidgets import QMainWindow
from typing import Dict

from clnt.GUI.GUIs.camera_GUI import CameraGUI
from clnt.GUI.GUIs.friendsGUI import FriendsGUI
from clnt.GUI.GUIs.loginGUI import LoginGUI
from clnt.GUI.GUIs.mainGUI import MainWindowGUI
from clnt.GUI.GUIs.registerGUI import RegisterGUI
from clnt.GUI.GUIs.window_names import WindowNames

WINDOWS_MAPPING: Dict[WindowNames, type(QMainWindow)] = {
    WindowNames.LOGIN: LoginGUI,
    WindowNames.REGISTER: RegisterGUI,
    WindowNames.CAMERA: CameraGUI,
    WindowNames.MAIN: MainWindowGUI,
    WindowNames.FRIENDS: FriendsGUI
}
