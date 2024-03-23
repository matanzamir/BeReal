"""
Matan Zamir

camera gui window
"""
import socket

import cv2
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from clnt.GUI.GUIs.gui_inteface import GUIInterface
from clnt.GUI.GUIs.window_names import WindowNames
from clnt.protocol import Protocol
import threading

from clnt.recv_options import Recv
from clnt.server_ops import ServerOps
from clnt.GUI.GUIs.gui_constants import *


class CameraGUI(QMainWindow, GUIInterface):
    """
    camera gui class
    """

    def __init__(self, parent):
        """
        constructor for the camera window
        """
        super().__init__(parent)
        uic.loadUi("GUI\\UIs\\cameraUI.ui", self)
        self.parent = parent
        self.on = True
        self.cam = None
        self.initiate_cam()
        self.image = None
        self.cam_thread = None
        self.end_thread = False
        self.confirmButton.clicked.connect(self.confirmed)
        self.anotherPicButton.clicked.connect(self.start_cam)

    def camera_loop(self):
        """
        displaying camera and capturing image
        """
        try:
            while True:
                if self.cam:
                    self.start_loop_buttons()
                    self.on = True
                    while True:
                        ret, frame = self.cam.read()
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        height, width, channel = frame.shape
                        q_image = QImage(frame.data,
                                         width,
                                         height,
                                         channel * width,
                                         QImage.Format_RGB888)
                        self.cameraLabel.setPixmap(QPixmap.fromImage(q_image))
                        if not self.on:
                            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            bytes_image = cv2.imencode(".jpeg", frame)
                            self.image = bytes_image[ARR_POS_1].tobytes()
                            break
                    self.end_loop_buttons()
                    break
        except RuntimeError as e:
            print(e)

    def start_loop_buttons(self):
        """
        showing/ hiding buttons at the start of the camera loop
        """
        if self.Button.isHidden():
            self.Button.show()
        if not self.anotherPicButton.isHidden() and not \
                self.confirmButton.isHidden():
            self.anotherPicButton.hide()
            self.confirmButton.hide()

    def end_loop_buttons(self):
        """
        showing/ hiding buttons at the end of the camera loop
        """
        if not self.Button.isHidden():
            self.Button.hide()
        if self.anotherPicButton.isHidden() and self.confirmButton.isHidden():
            self.anotherPicButton.show()
            self.confirmButton.show()

    def end(self):
        """
        ending camera loop
        """
        self.on = False

    def confirmed(self):
        """
        confirmed image event, sends image to server
        """
        try:
            self.parent.client.socket.send(Recv.TEXT + ServerOps.IMAGE)
            Protocol.send_image(self.parent.client.socket,
                                self.image,
                                self.parent.client.username)
            del self.cam
            self.parent.window_call(WindowNames.MAIN)
        except socket.error as e:
            self.parent.client.socket.close()
            print(e)
            self.error_label.setText(ERROR_MESSAGE)
        except Exception as e:
            print(e)

    def initiate_cam(self):
        """
        initiating camera
        """
        cam = cv2.VideoCapture(VIDEO)
        ret, frame = cam.read()
        if frame is not None:
            self.Button.setText('capture')
            self.Button.clicked.connect(self.end)
            self.cam = cam
        else:
            print('camera in use')
            self.Button.setText('try again')
            self.Button.clicked.connect(self.initiate_cam)
            self.cameraLabel.setText('camera in use. please try again')
            self.confirmButton.hide()
            self.anotherPicButton.hide()
            self.cam = None

    def start_cam(self):
        """
        starting camera thread
        """
        self.cam_thread = threading.Thread(target=self.camera_loop)
        self.cam_thread.start()

    def bereal_filter(self):
        """
        filtering bereal requests
        """
        while True:
            try:
                Protocol.receive(Recv.GHOST, self.parent.client.listen_socket)
                if self.end_thread:
                    return
            except socket.error as e:
                self.parent.client.socket.close()
            except AttributeError:
                pass

    def start(self):
        """
        starting functions
        """
        thr = threading.Thread(target=self.bereal_filter)
        thr.start()
        self.start_cam()

    def stop(self):
        """
        stopping functions
        """
        try:
            self.end_thread = True
            self.parent.client.socket.send(Recv.TEXT + ServerOps.GHOST)
        except socket.error as e:
            self.parent.client.socket.close()
            print(e)
