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

        # IA TFLite
        if self.model:
            try:
                input_details = self.model.get_input_details()
                output_details = self.model.get_output_details()

                img = cv2.resize(frame, (128, 128))
                img = img.astype(np.float32) / 255.0
                img = np.expand_dims(img, axis=0)

                self.model.set_tensor(input_details[0]['index'], img)
                self.model.invoke()
                mask = self.model.get_tensor(output_details[0]['index'])[0]

                # Normalisation + resize
                mask = np.clip(mask, 0, 1)
                mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))

                mask = (mask > 0.5).astype(np.uint8) * 255
                mask = cv2.medianBlur(mask, 5)
                return mask

            except Exception:
                # fallback automatique
                self.model = None

        # Fallback OpenCV HSV (laser rouge)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower1 = np.array([0, 120, 120])
        upper1 = np.array([10, 255, 255])

        lower2 = np.array([170, 120, 120])
        upper2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower1, upper1)
        mask2 = cv2.inRange(hsv, lower2, upper2)

        mask = cv2.bitwise_or(mask1, mask2)
        mask = cv2.medianBlur(mask, 5)

        return mask
