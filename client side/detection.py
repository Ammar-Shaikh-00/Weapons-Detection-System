from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QImage
import cv2
import numpy as np
import time
import requests
import torch
from torchvision import transforms
from models.experimental import attempt_load # type: ignore
from utils.general import non_max_suppression, scale_coords # type: ignore
from utils.datasets import letterbox # type: ignore
from utils.plots import plot_one_box # type: ignore

class Detection(QThread):
    def __init__(self, token, location, receiver):
        super(Detection, self).__init__()
        self.token = token
        self.location = location
        self.receiver = receiver

    changePixmap = pyqtSignal(QImage)    

    def run(self):
        self.running = True
        
        # Load model
        model = attempt_load('yolov7.pt', map_location='cpu')

        # Assuming 'names' is a list of class names
        names = model.names if hasattr(model, 'names') else model.module.names
        #self.classes = model.names if hasattr(model, 'names') else model.module.names

        # Generate random colors for each class
        colors = [[np.random.randint(0, 255) for _ in range(3)] for _ in names]

        # Open video file
        cap = cv2.VideoCapture(0)

        # Define codec and create VideoWriter object to save the result
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

        starting_time = time.time() - 11

        while self.running:
            ret, frame = cap.read()
            if ret:
                height, width, channels = frame.shape
                #image = self.transform(frame).unsqueeze(0)  # Add batch dimension
            else:
                break

            img0 = frame.copy()  # Copy the frame for drawing
            img = letterbox(frame, new_shape=640)[0]
            img = img[:, :, ::-1].transpose(2, 0, 1)
            img = np.ascontiguousarray(img)

            # Prepare image for inference
            img = torch.from_numpy(img).float()
            img /= 255.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Inference
            with torch.no_grad():
                pred = model(img, augment=False)[0]
                pred = non_max_suppression(pred, 0.5, 0.45, classes=None, agnostic=False)

            # Process detections
            for i, det in enumerate(pred):
                if len(det):
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()
                    for *xyxy, conf, cls in reversed(det):
                        label = f'{names[int(cls)]} {conf:.2f}'
                        plot_one_box(xyxy, img0, label=label, color=colors[int(cls)], line_thickness=2)
                        if int(cls) == 0:
                            elapsed_time = starting_time - time.time()

                            if elapsed_time <= -10:
                                starting_time = time.time()
                                self.save_detection(img0)



            # Write the frame with detections to the output video
            out.write(img0)
 
            width = width

            rgbImage = cv2.cvtColor(img0, cv2.COLOR_BGR2RGB)
            bytesPerLine = channels * width 
            convertToQtFormat = QImage(rgbImage.data, width, height, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(854, 854, Qt.KeepAspectRatio) #854
            self.changePixmap.emit(p)
    
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
    

