import numpy as np
import cv2

class LaserAI:
    def __init__(self, tflite_path=None):
        self.model = None
        if tflite_path:
            try:
                import tflite_runtime.interpreter as tflite
                self.model = tflite.Interpreter(model_path=tflite_path)
                self.model.allocate_tensors()
            except Exception:
                self.model = None

    def detect(self, frame):
        if frame is None:
            return None

        # Si modèle IA disponible → TFLite
        if self.model:
            input_details = self.model.get_input_details()
            output_details = self.model.get_output_details()

            img = cv2.resize(frame, (128, 128))
            img = img.astype(np.float32) / 255.0
            img = np.expand_dims(img, axis=0)

            self.model.set_tensor(input_details[0]['index'], img)
            self.model.invoke()
            mask = self.model.get_tensor(output_details[0]['index'])[0]

            mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
            return (mask > 0.5).astype(np.uint8) * 255

        # Sinon → fallback OpenCV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 120, 120])
        upper_red = np.array([10, 255, 255])
        return cv2.inRange(hsv, lower_red, upper_red)
