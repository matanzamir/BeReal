"""
Matan Zamir

friends gui window
"""
import socket
from functools import partial

from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import \
    QMainWindow, QGroupBox, QLabel, QPushButton, QHBoxLayout

from clnt.GUI.GUIs.gui_inteface import GUIInterface
from clnt.GUI.GUIs.gui_protocol import GUIProtocol
from clnt.GUI.GUIs.window_names import WindowNames
from clnt.protocol import Protocol
from clnt.recv_options import Recv
from clnt.server_ops import ServerOps
from clnt.operators import *
from clnt.GUI.GUIs.gui_constants import *


class FriendsGUI(QMainWindow, GUIInterface):
    """
    friends gui class
    """
    def __init__(self, parent):
        """
        constructor for friends window
        """
        super().__init__(parent)
        uic.loadUi("GUI\\UIs\\friendsUI.ui", self)
        self.parent = parent
        self.users_gb = {}
        self.friends_gb = {}
        self.friends_list = []
        self.users_list = []
        self.check_timer = None
        self.presented = False
        self.friendsLayout.setAlignment(Qt.AlignTop)
        self.logo.setText(f'{self.parent.client.username} friends')
        self.usersLayout.setAlignment(Qt.AlignTop)
        self.backButton.clicked.connect(self.back)
        self.searchLine.textChanged.connect(self.load_users)
        GUIProtocol.line_edit_validator(self.searchLine)

    def create_user(self, user, operation):
        """
        creating a new user groupbox
        """
        gb = QGroupBox()
        label = QLabel(user)
        button = QPushButton(operation)
        gb_layout = QHBoxLayout()
        gb.setLayout(gb_layout)
        gb_layout.addWidget(label)
        gb_layout.addWidget(button)
        gb.setFixedHeight(FRIEND_HEIGHT)
        button.clicked.connect(partial(getattr(self, operation), user))
        return gb

    def load_users(self):
        """
        loading and displaying them, happens every second
        """
        try:
            self.parent.client.socket.send(Recv.TEXT +
                                           self.searchLine.text().encode() +
                                           SPLIT.encode() + ServerOps.SEARCH)
            string = Protocol.receive(Recv.TEXT,
                                      self.parent.client.listen_socket)
            if string == Recv.BEREAL:
                self.parent.window_call(WindowNames.CAMERA)
            elif string:
                friends_list, users_list = string.split(SAP)
                friends_list = friends_list.split(PARAMS)
                users_list = users_list.split(PARAMS)
                self.delete_all()
                self.add_friends(friends_list)
                self.add_users(users_list)
                self.add_widgets()
        except socket.error as e:
            self.parent.client.socket.close()
            print(e)
            self.error_label.setText(ERROR_MESSAGE)
        except Exception as e:
            print(e)

    def delete_all(self):
        """
        deleting all gbs on screen
        """
        for gb in self.users_gb:
            self.users_gb[gb].deleteLater()
            self.users_gb[gb] = None
        self.users_gb = {}
        self.users_list = []
        for gb in self.friends_gb:
            self.friends_gb[gb].deleteLater()
            self.friends_gb[gb] = None
        self.friends_gb = {}
        self.friends_list = []

    def add_friends(self, friends_list):
        """
        adding all friends to friends list
        """
        for friend in friends_list:
            if friend and friend not in self.friends_list:
                self.friends_list.append(friend)
                self.friends_gb[friend] = self.create_user(friend, 'unfriend')
                self.friends_gb = dict(sorted(self.friends_gb.items()))

    def add_users(self, users_list):
        """
        adding all users to users list
        """
        for user in users_list:
            if user and user not in self.users_list:
                self.users_list.append(user)
                self.users_gb[user] = self.create_user(user, 'add')
                self.users_gb = dict(sorted(self.users_gb.items()))

    def add_widgets(self):
        """
        displaying created users groupboxes
        """
        for user in self.users_gb:
            self.usersLayout.addWidget(self.users_gb[user])
        for friend in self.friends_gb:
            self.friendsLayout.addWidget(self.friends_gb[friend])

    def unfriend(self, user):
        """
        unfriend button event, unfriending user
        """
        try:
            request = f'{user}{SPLIT}unfriend{EOT}'.encode()
            self.parent.client.socket.send(Recv.TEXT + request)
            self.friends_gb[user].deleteLater()
            del self.friends_gb[user]
            self.friends_list.remove(user)
        except socket.error as e:
            self.parent.client.socket.close()
            print(e)
            self.error_label.setText(ERROR_MESSAGE)

    def add(self, user):
        """
        add button event, adding user as friend
        """
        try:
            self.parent.client.socket.send(Recv.TEXT +
                                           f'{user}{SPLIT}add{EOT}'.encode())
            self.users_gb[user].deleteLater()
            del self.users_gb[user]
            self.users_list.remove(user)
        except socket.error as e:
            self.parent.client.socket.close()
            print(e)
            self.error_label.setText(ERROR_MESSAGE)
        except Exception as e:
            print(e)

    def back(self):
        """
        back button event, returns to main screen
        """
        self.parent.window_call(WindowNames.MAIN)

    def start(self):
        """
        starting function
        """
        self.load_users()
        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.load_users)
        self.check_timer.start(TIMER)

    def stop(self):
        """
        stopping function
        """
        if self.check_timer:
            self.check_timer.stop()
