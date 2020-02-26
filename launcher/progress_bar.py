import os
import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import threading
import requests
import psutil


class Download_Thread(threading.Thread):
    def __init__(self, url, file_name, window):
        threading.Thread.__init__(self)
        self.url = url
        self.file = file_name
        self.window = window

    def run(self):
        r = requests.get(self.url, stream=True)
        self.file_size = int(r.headers.get('content-length'))
        if not self.check_space():
            pass
        else:
            path = os.path.join(os.getcwd(), self.file)
            with open(path, 'wb') as file:
                file.write(r.content)
                dl = 0
                for data in r.iter_content():
                    dl += len(data)
                    file.write(data)
                    done = int(100*dl/self.file_size)
                    self.window.setProgress(done)
            return

    def check_space(self):
        disk_space = psutil.disk_usage('/')[2]
        return self.file_size < disk_space


class DownloadingWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle('Downloading Albion Meter')
        layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

        self.setGeometry(300, 300, 300, 50)

    def setProgress(self, value):
        if value > 100:
            value = 100
        self.progress_bar.setValue(value)

    def closeEvent(self, event):
        sys.exit(0)


def check_platform():
    system = sys.platform
    if system == 'win32':
        link = 'https://github.com/mazurwiktor/albion-online-stats/releases/download/0.8.1/albion-online-stats.exe'
    else:
        link = 'https://github.com/mazurwiktor/albion-online-stats/releases/download/0.8.1/albion-online-stats-linux'

    return link


if __name__ == '__main__':
    app = QApplication()
    w = DownloadingWindow()
    w.show()

    link = check_platform()
    file_name = 'albion-meter'
    Download_Thread(link, file_name, w).start()

    app.exec_()
    sys.exit(app.exec_())