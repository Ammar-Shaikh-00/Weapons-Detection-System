import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'yolov7'))

from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = LoginWindow()
    mainwindow.show()
    sys.exit(app.exec_())
