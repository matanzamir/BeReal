"""
Matan Zamir

main screen gui window
"""
import socket
import threading

from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import \
    QMainWindow, QLabel, QVBoxLayout, QSplitter, QGroupBox

from clnt.GUI.GUIs.gui_inteface import GUIInterface
from clnt.GUI.GUIs.window_names import WindowNames
from clnt.recv_options import Recv
from clnt.server_ops import ServerOps
from clnt.protocol import Protocol
from clnt.operators import *
from clnt.GUI.GUIs.gui_constants import *


class MainWindowGUI(QMainWindow, GUIInterface):
    """
    main screen window class
    """
    def __init__(self, parent):
        """
        main screen window constructor
        """
        super().__init__(parent)
        uic.loadUi("GUI\\UIs\\main_screenUI.ui", self)
        self.parent = parent
        self.end_thread = False
        self.image_gbs = []
        self.new_images = []
        self.listen_thread = None
        self.timer = None
        self.logo.setText(f'{self.parent.client.username} main')
        self.logOutButton.clicked.connect(self.log_out)
        self.friendsButton.clicked.connect(self.friends_gui)
        self.photosLayout.setAlignment(Qt.AlignHCenter)

    def add_image(self, user, photo):
        """
        adding an image groupbox
        """
        gb = QGroupBox(user)
        pixmap = QPixmap()
        pixmap.loadFromData(photo)
        photo = QLabel()
        photo.setPixmap(pixmap)
        gb_layout = QVBoxLayout()
        gb.setLayout(gb_layout)
        gb_layout.addWidget(photo)
        photo.setScaledContents(True)
        width, height = self.get_dimensions(pixmap)
        gb.setFixedSize(width, height)
        font = QFont()
        font.setPointSize(FONT_SIZE)
        font.setBold(True)
        gb.setFont(font)
        gb.setAlignment(Qt.AlignCenter)
        self.image_gbs.append(gb)

    def listen_to_photos(self):
        """
        listens to photos
        """
        while True:
            try:
                user, bin_image = \
                    Protocol.receive(Recv.IMAGE,
                                     self.parent.client.listen_socket)
                print('received ', user, ' image')
                if bin_image:
                    self.new_images.append((user, bin_image))
                if self.end_thread:
                    return
            except socket.error as e:
                self.parent.client.socket.close()
                self.error_label.setText(ERROR_MESSAGE)
            except Exception as e:
                print(e)

    @staticmethod
    def get_dimensions(pixmap):
        """
        changing the dimensions of the image accordingly
        """
        width, height = pixmap.width(), pixmap.height()
        ratio = RATIO / width
        width = width * ratio
        height = height * ratio
        return round(width), round(height)

    def load_images(self):
        """
        loading images and showing them on screen, happens every second
        """
        if self.new_images:
            for image in self.new_images:
                if image[ARR_POS_1] == Recv.BEREAL:
                    self.end_thread = True
                    self.parent.client.socket.send(Recv.TEXT + ServerOps.GHOST)
                    self.parent.window_call(WindowNames.CAMERA)
                elif image:
                    self.add_image(image[ARR_POS_0], image[ARR_POS_1])
            self.new_images = []
            self.add_photos()
        if self.image_gbs and not self.status_label.isHidden():
            self.status_label.hide()

    def add_photos(self):
        """
        adding photos to main screen
        """
        for image_gb in self.image_gbs:
            self.photosLayout.addWidget(image_gb)
            splitter = QSplitter(Qt.Horizontal)
            self.photosLayout.addWidget(splitter)
            image_gb.setAlignment(Qt.AlignCenter)

    def log_out(self):
        """
        log out button event, logging out and calling log out screen
        """
        try:
            self.end_thread = True
            self.parent.client.socket.send(Recv.TEXT +
                                           f'log out{SPLIT}'.encode() +
                                           ServerOps.CONNECT)
            self.parent.window_call(WindowNames.LOGIN)
        except socket.error as e:
            self.parent.client.socket.close()
            print(e)
            self.parent.window_call(WindowNames.LOGIN)

    def friends_gui(self):
        """
        friends button event, calling friends window
        """
        try:
            self.end_thread = True
            self.parent.client.socket.send(Recv.TEXT + ServerOps.GHOST)
            self.parent.window_call(WindowNames.FRIENDS)
        except socket.error as e:
            self.parent.client.socket.close()
            print(e)
            self.parent.window_call(WindowNames.FRIENDS)

    def start(self):
        """
        staring functions
        """
        try:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.load_images)
            self.timer.start(TIMER)
            self.listen_thread = threading.Thread(target=self.listen_to_photos)
            self.listen_thread.start()
            self.parent.client.socket.send(Recv.TEXT + ServerOps.IMAGES)
        except socket.error as e:
            self.parent.client.socket.close()
            print(e)
            self.error_label.setText(ERROR_MESSAGE)

    def stop(self):
        """
        stopping function
        """
        if self.timer:
            self.timer.stop()
        self.new_images = []
        self.image_gbs = []
