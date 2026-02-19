import wx
import cv2
from horus.engine.camera import Camera
from horus.calibration.laser_calibration import LaserCalibration
from horus.utils.calibration_store import CalibrationStore

class CalibrationPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.camera = Camera()
        self.calib = LaserCalibration()

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

    def capture_frame(self):
        self.camera.open()
        frame = self.camera.read()
        self.camera.close()
        return frame

    def show_image(self, frame):
        if frame is None:
            return
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w = rgb.shape[:2]
        img = wx.Image(w, h, rgb.tobytes())
        self.bitmap.SetBitmap(wx.Bitmap(img))

    def on_left(self, event):
        frame = self.capture_frame()
        if frame is None:
            wx.MessageBox("Erreur : impossible de capturer une image", "Erreur")
            return
        plane = self.calib.calibrate_left_laser(frame)
        CalibrationStore.save("left_laser", plane)
        self.show_image(frame)
        wx.MessageBox(f"Laser gauche calibré : {plane}", "OK")

    def on_right(self, event):
        frame = self.capture_frame()
        if frame is None:
            wx.MessageBox("Erreur : impossible de capturer une image", "Erreur")
            return
        plane = self.calib.calibrate_right_laser(frame)
        CalibrationStore.save("right_laser", plane)
        self.show_image(frame)
        wx.MessageBox(f"Laser droit calibré : {plane}", "OK")
