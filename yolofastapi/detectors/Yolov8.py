import torch
import numpy as np
import cv2
import os
import platform
from ultralytics import YOLO
from PIL import Image

class Yolov8:
    PATH = os.environ.get("YOLO_WEIGHTS_PATH", "yolov8n.pt")
    CONF_thres = float(os.environ.get("YOLO_CONF_THRESHOLD", "0.5"))

    def __init__(self, chunked: bytes = None):
        self._bytes = chunked
        self.model = self._load_model()
        self.device = self._get_device()
        self.classes = self.model.names

    def _get_device(self):
        if platform.system().lower() == "darwin":
            return "mps"
        if torch.cuda.is_available():
            return "cuda"
        return "cpu"
    
    def _load_model(self):
        model = YOLO(Yolov8.PATH)
        return model
    
    async def __call__(self):
        frame = self._get_image_from_chunked()
        results = self.score_frame(frame)
        frame, labels = self.plot_boxes(results, frame)
        return frame, set(labels)
    
    def _get_image_from_chunked(self):
        arr = np.asarray(bytearray(self._bytes), dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED) 
        return img
    
    def score_frame(self, frame):
        self.model.to(self.device)
        frame = [frame]
        results = self.model(   
            frame,
            conf=Yolov8.CONF_thres,
            save_conf=True
        )
        return results
    
    def class_to_label(self, x):
        return self.classes[int(x)]
    
    def plot_boxes(self, results, frame):
        labels = []
        image_height, image_width = frame.shape[:2]

        for r in results:
            boxes = r.boxes
            for box in boxes:
                class_id = int(box.cls)
                label = self.model.names[class_id]
                labels.append(label)
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                font_scale = min(image_width, image_height) / 500  
                font_thickness = max(1, int(min(image_width, image_height) / 100))
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                            font_scale, (0, 255, 0), font_thickness)
        
        return frame, labels