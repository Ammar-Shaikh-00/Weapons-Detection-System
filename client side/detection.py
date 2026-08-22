from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QImage
import cv2
import numpy as np
import time
import requests
import torch
from yolov7.models.experimental import attempt_load # type: ignore
from yolov7.utils.general import non_max_suppression, scale_coords # type: ignore
from yolov7.utils.datasets import letterbox
from yolov7.utils.plots import plot_one_box # type: ignore

class Detection(QThread):
    def __init__(self, token, location, receiver):
        super(Detection, self).__init__()
        self.token = token
        self.location = location
        self.receiver = receiver

    changePixmap = pyqtSignal(QImage)    

    def run(self):
        self.running = True
        cap = None

        try:
            print('Loading detection model...')
            model = attempt_load('best_50.pt', map_location='cpu')
            names = model.names if hasattr(model, 'names') else model.module.names
            if isinstance(names, dict):
                names = [names[i] for i in range(len(names))]
            colors = [[np.random.randint(0, 255) for _ in range(3)] for _ in names]

            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not cap.isOpened():
                cap.release()
                cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print('Failed to open camera')
                return
            print('Camera opened')

            starting_time = time.time() - 11

            while self.running:
                ret, frame = cap.read()
                if not ret or frame is None:
                    print('Failed to read camera frame')
                    break

                height, width, channels = frame.shape
                img0 = frame.copy()
                img = letterbox(frame, new_shape=640)[0]
                img = img[:, :, ::-1].transpose(2, 0, 1)
                img = np.ascontiguousarray(img)

                img = torch.from_numpy(img).float()
                img /= 255.0
                if img.ndimension() == 3:
                    img = img.unsqueeze(0)

                with torch.no_grad():
                    pred = model(img, augment=False)[0]
                    pred = non_max_suppression(pred, 0.5, 0.45, classes=None, agnostic=False)

                for i, det in enumerate(pred):
                    if len(det):
                        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()
                        for *xyxy, conf, cls in reversed(det):
                            class_id = int(cls)
                            label = f'{names[class_id]} {conf:.2f}'
                            plot_one_box(xyxy, img0, label=label, color=colors[class_id], line_thickness=2)
                            if class_id == 0:
                                elapsed_time = starting_time - time.time()
                                if elapsed_time <= -10:
                                    starting_time = time.time()
                                    self.save_detection(img0)

                rgbImage = np.ascontiguousarray(cv2.cvtColor(img0, cv2.COLOR_BGR2RGB))
                bytesPerLine = channels * width
                convertToQtFormat = QImage(
                    rgbImage.data, width, height, bytesPerLine, QImage.Format_RGB888
                ).copy()
                p = convertToQtFormat.scaled(854, 854, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
        except Exception as e:
            print(f'Detection thread error: {e}')
        finally:
            if cap is not None:
                cap.release()
            print('Detection thread stopped')
    
    def save_detection(self, frame):
        cv2.imwrite("saved_frame/frame.jpg", frame)
        print('Frame saved')
        self.post_detection()

    def post_detection(self):
        try:
            url = 'http://127.0.0.1:8000/api/images/'
            headers = {'Authorization': 'Token ' + self.token}
            files = {'image': open('saved_frame/frame.jpg', 'rb')}
            data = {'user_ID': self.token, 'location': self.location, 'alert_receiver': self.receiver}
            response = requests.post(url, files=files, headers=headers, data=data)
        
        # HTTP 200
            if response.ok:
                print('Alert was sent to the server')
        # Bad response
            else:
                print('Unable to send alert to the server')

        except Exception as e:
            print(e)
            print('Unable to access server')
    

