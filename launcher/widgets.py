import sys
import os
from PySide2.QtCore import Slot
from PySide2.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton,QVBoxLayout, QWidget)
import launcher.helpers
import threading
import subprocess


class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.items = 0
        self.latest = launcher.helpers.latest_version()

        # Left
        self.right = QVBoxLayout()
        self.label1 = QLabel("Looking for updates...")
        self.right.addWidget(self.label1)

        self.download = QPushButton("Download")
        self.run = QPushButton("Run")
        self.right.addWidget(self.download)
        self.download.setEnabled(False)
        self.right.addWidget(self.run)
        self.run.setEnabled(False)

        # QWidget Layout
        self.layout = QHBoxLayout()

        # self.table_view.setSizePolicy(size)
        self.layout.addLayout(self.right)

        # Set the layout to the QWidget
        self.setLayout(self.layout)

        # Signals and Slots
        self.download.clicked.connect(self.download_latest)
        self.run.clicked.connect(self.run_meter)


        if launcher.helpers.check_version(self.latest) == None:
            self.label1.setText("Click Download to update.")
            self.download.setEnabled(True)
        elif launcher.helpers.check_version(latest=self.latest):
            self.label1.setText("Ready to update.")
            self.download.setEnabled(True)
            self.run.setEnabled(True)
        else:
            self.label1.setText("You've got latest version.")
            self.run.setEnabled(True)


    @Slot()
    def download_latest(self):
        Watek().start()
        self.label1.setText("Downloading...")
        self.download.setEnabled(False)
        self.run.setEnabled(False)

    @Slot()
    def run_meter(self):
        print("runinng app")
        subprocess.Popen('./albion-online-stats-linux')
        sys.exit(0)


class Watek(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        path = os.path.join(os.getcwd(), 'albion-online-stats-linux')
        launcher.helpers.download(path)
        launcher.helpers.version_file(launcher.helpers.latest_version())
        Widget().run_meter()
        return 0

class Window(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Launcher")
        self.setCentralWidget(widget)


if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    # QWidget
    widget = Widget()
    # QMainWindow using QWidget as central widget
    window = Window(widget)
    window.resize(200, 100)
    window.show()


    # Execute application
    sys.exit(app.exec_())
