import sys

import cv2
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class VideoThread(QThread):
    video = pyqtSignal(object)

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        camera = cv2.VideoCapture(0)

        if camera.isOpened():
            video_open, frame = camera.read()
            if video_open:
                cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)
                width, height, _ = frame.shape
                image = QImage(
                    frame.data, height, width, QImage.Format_RGB888)
                self.video.emit(image)
        else:
            self.video.emit('failed')


class MainWindow(QMainWindow):
    def __init__(self):
        QWidget.__init__(self, None)
        self.video_label = QLabel(self)
        self.video_label.show()

        layout = QVBoxLayout()
        layout.addWidget(self.create_crop_controls())
        layout.addWidget(self.video_label)

        window = QWidget()
        window.setLayout(layout)

        self.setCentralWidget(window)

        self.setWindowTitle('"Pixels: Test your memory" Bot')

        self.video_thread = VideoThread()
        self.video_thread.video.connect(self.on_frame_ready)
        self.video_thread.start()

    def create_crop_controls(self):
        layout = QVBoxLayout()

        def create_crop_control(text):
            layout = QHBoxLayout()
            layout.addWidget(QLabel(text))
            layout.addWidget(QSpinBox())

            control = QWidget()
            control.setLayout(layout)
            return control

        layout.addWidget(create_crop_control('Left'))
        layout.addWidget(create_crop_control('Right'))
        layout.addWidget(create_crop_control('Top'))
        layout.addWidget(create_crop_control('Bottom'))

        crop_controls = QWidget()
        crop_controls.setLayout(layout)
        return crop_controls

    def on_frame_ready(self, frame):
        if frame == 'failed':
            print 'Video failed'
            return
        if self.video_label.width() != frame.width() or self.video_label.height() != frame.height():
            print 'adjust size'
            self.video_label.setFixedSize(frame.width(), frame.height())
        self.video_label.setPixmap(QPixmap(frame))
        self.video_thread.start()


def start():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setFixedSize(800, 800)
    window.show()

    sys.exit(app.exec_())
