from PyQt5.QtWidgets import QApplication
import sys
sys.path.append("C:/Users/Internee.BRK0650/yolov7")
from login_window import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = LoginWindow()
    
    mainwindow.show()
    sys.exit(app.exec_())

'''app = QApplication(sys.argv)
mainwindow = LoginWindow()
mainwindow.show()
sys.exit(app.exec_())
'''