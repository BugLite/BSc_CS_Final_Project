import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import os

class WebcamDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Webcam Dashboard')

        # Create buttons for different feeds
        live_feed_button = QPushButton('Live Feed', self)
        live_feed_button.clicked.connect(self.open_live_feed)

        detector1_button = QPushButton('Detector 1', self)
        detector1_button.clicked.connect(self.open_detector1)

        detector2_button = QPushButton('Detector 2', self)
        detector2_button.clicked.connect(self.open_detector2)

        # Create layout and add buttons
        layout = QVBoxLayout()
        layout.addWidget(live_feed_button)
        layout.addWidget(detector1_button)
        layout.addWidget(detector2_button)

        self.setLayout(layout)
        self.show()

    def open_live_feed(self):
        os.system("/opt/homebrew/bin/python3.11 live_feed.py")

    def open_detector1(self):
        os.system("/opt/homebrew/bin/python3.11 detector_1.py")

    def open_detector2(self):
        os.system("/opt/homebrew/bin/python3.11 detector_2.py")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WebcamDashboard()
    sys.exit(app.exec_())
