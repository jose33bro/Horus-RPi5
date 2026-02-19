import wx
import cv2
import numpy as np

from horus.engine.camera import Camera
from horus.engine.grbl_controller import GRBLController
from horus.calibration.laser_calibration import LaserCalibration
from horus.utils.calibration_store import CalibrationStore

class CalibrationPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.camera = Camera()
        self.grbl = GRBLController()
        self.calib = LaserCalibration()
        self.store = CalibrationStore()

        vbox = wx.BoxSizer(wx.VERTICAL)

        btn_left = wx.Button(self, label="Calibrer laser gauche")
        btn_right = wx.Button(self, label="Calibrer laser droit")

        btn_left.Bind(wx.EVT_BUTTON, self.on_left)
        btn_right.Bind(wx.EVT_BUTTON, self.on_right)

        vbox.Add(btn_left, 0, wx.ALL, 5)
        vbox.Add(btn_right, 0, wx.ALL, 5)

        self.bitmap = wx.StaticBitmap(self)
        vbox.Add(self.bitmap, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(vbox)

    def capture(self):
        """Capture propre avec ouverture/fermeture sécurisée."""
        try:
            self.camera.open()
            frame = self.camera.read()
            self.camera.close()
            return frame
        except Exception:
            return None

    def show_overlay(self, frame, mask):
        """Affiche l'image avec overlay laser."""
        if frame is None:
            return

        overlay = frame.copy()
        overlay[mask > 0] = (0, 255, 0)  # laser en vert

        rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
        h, w = rgb.shape[:2]
        img = wx.Image(w, h, rgb.tobytes())
        self.bitmap.SetBitmap(wx.Bitmap(img))

    def calibrate(self, side):
        """Calibrage générique gauche/droit."""
        try:
            self.grbl.connect()

            # Laser ON
            if side == "left":
                self.grbl.set_laser(left=True)
            else:
                self.grbl.set_laser(right=True)

            frame = self.capture()

            # Laser OFF
            self.grbl.set_laser()

            if frame is None:
                wx.MessageBox("Impossible de capturer une image", "Erreur")
                return

            if side == "left":
                plane, mask = self.calib.calibrate_left_laser(frame)
                self.store.save(plane, None)
            else:
                plane, mask = self.calib.calibrate_right_laser(frame)
                self.store.save(None, plane)

            self.show_overlay(frame, mask)
            wx.MessageBox(f"Laser {side} calibré : {plane}", "OK")

        except Exception as e:
            wx.MessageBox(str(e), "Erreur calibration")
        finally:
            self.grbl.disconnect()

    def on_left(self, event):
        self.calibrate("left")

    def on_right(self, event):
        self.calibrate("right")
