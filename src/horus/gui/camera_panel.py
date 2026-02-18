import wx
import cv2
import numpy as np
from horus.engine.camera import Camera

class CameraPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.camera = Camera()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_frame, self.timer)

        self.bitmap = wx.StaticBitmap(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.bitmap, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def start(self):
        try:
            self.camera.open()
            self.timer.Start(30)  # ~33 FPS
        except Exception as e:
            wx.MessageBox(str(e), "Erreur caméra", wx.OK | wx.ICON_ERROR)

    def stop(self):
        self.timer.Stop()
        self.camera.close()

    def update_frame(self, event):
        frame = self.camera.read()

        # Convertir BGR → RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        h, w = frame.shape[:2]
        image = wx.Image(w, h, frame.tobytes())
        self.bitmap.SetBitmap(wx.Bitmap(image))
        self.Refresh()
