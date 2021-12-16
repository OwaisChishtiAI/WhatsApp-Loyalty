from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import cv2

class ReceiptClassifier:
    def __init__(self, customer_number) -> None:
        self.customer_number = customer_number

    def preprocess(self):
        NotImplementedError()

    def train(self):
        NotImplementedError()

    def predict(self):
        np.set_printoptions(suppress=True)
        model = load_model(r'model\label\keras_model.h5')
        labels = {0: "imtiaz", 1: "kfc", 2: "walmart"}
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image = Image.open(f"uploads/{self.customer_number}/.jpg")
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        prediction = model.predict(data)
        print("[INFO] Raw Predictions ", prediction)
        y_hat = np.argmax(prediction[0])
        proba = prediction[0][y_hat] * 100
        print("[INFO] Predictions, ", y_hat, proba, labels[y_hat])
        if proba > 80:
            return labels[y_hat]
        else:
            return ""