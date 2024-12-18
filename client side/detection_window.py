from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from detection import Detection

class DetectionWindow(QMainWindow):
    def __init__(self, token):
        super(DetectionWindow, self).__init__()
        loadUi('UI/detection_window.ui', self)
        # Initialize the Detection instance

        self.token = token
        
        # Connecting buttons to their respective functions
        self.stop_detection_button.clicked.connect(self.close)

        # Create the detection instance
        #self.create_detection_instance(self.token, self.location, self.receiver)

    def create_detection_instance(self, token, location, receiver):
        # Initialize the detection instance
        self.detection = Detection(token, location, receiver)

    @pyqtSlot(QImage)
    def setImage(self, image):
        # Slot to update the QLabel with the new image
        self.label_detection.setPixmap(QPixmap.fromImage(image))

    def start_detection(self):
        # Ensure that detection instance is created
        if not hasattr(self, 'detection'):
            self.create_detection_instance()
        
        # Connect the detection signal to update the image
        self.detection.changePixmap.connect(self.setImage)
        
        # Start the detection process
        self.detection.start()

        # Show the detection window
        self.show()

    def closeEvent(self, event):
        # Stop the detection when closing the window
        self.detection.running = False
        event.accept()


'''
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from detection import Detection

class DetectionWindow(QMainWindow):
    def __init__(self):
        super(DetectionWindow, self).__init__()
        loadUi('UI/detection_window.ui', self)
        self.stop_detection_button.clicked.connect(self.close)

    def create_detection_instance(self):
        self.detection = Detection()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label_detection.setPixmap(QPixmap.fromImage(image))

    def start_detection(self):
        self.detection.changePixmap.connect(self.setImage)
        self.detection.start()
        self.show()

    def closeEvent(self, event):
        self.detection.running = False
        event.accept()

'''