import torch
import numpy as np
import cv2
import os
import platform
from ultralytics import YOLO
from PIL import Image
class Yolov3:
    PATH = os.environ.get("YOLO_WEIGHTS_PATH","yolov8n.pt")
    CONF_thres = float(os.environ.get("YOLO_CONF_THRESHOLD","0.78"))

    def __init__(self, chunked: bytes = None):
        self._bytes = chunked
        self.model = self._load_model()
        self.device = self._get_device()
        self.classes = self.model.names

    def _get_device(self):
        if platform.system().lower()=="darwin":
            return "mps"
        if torch.cuda.is_available():
            return "cuda"
        return "cpu"
    
    def _load_model(self):
        model = YOLO(Yolov3.PATH)
        return model
    
    async def __call__(self):
        frame = self._get_image_from_chunked()
        results = self.score_frame(frame)
        frame, labels = self.plot_boxes(results, frame)
        return frame, set(labels)
    
    def _get_image_from_chunked(self):
        arr = np.asarray(bytearray(self._bytes), dtype = np.uint8)
        img = cv2.imdecode(arr, -1)
        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        return img
    
    def score_frame(self, frame):
        self.model.to(self.device)
        frame = [frame]
        results = self.model(   
            frame,
            conf = Yolov3.CONF_thres,
            save_conf=True
        )
        return results
    
    def class_to_label(self, x):
        return self.classes[int(x)]
    
    def plot_boxes(self, results, frame):
        for r in results:
            boxes = r.boxes
            labels = []
            for box in boxes:
                c = box.cls
                l = self.model.names[int(c)]
                labels.append(l)
        frame = results[0].plot()
        return frame, labels