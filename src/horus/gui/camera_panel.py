import wx
import cv2
import numpy as np
from horus.engine.camera import Camera

class CameraPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # Utilise la classe Camera de Horus
        self.camera = Camera()

        # Timer pour rafraîchir l'image
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_frame, self.timer)

        # Zone d'affichage
        self.bitmap = wx.StaticBitmap(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.bitmap, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def start(self):
        """Démarre la caméra et le rafraîchissement."""
        try:
            self.camera.open()
            self.timer.Start(30)  # ~33 FPS
        except Exception as e:
            wx.MessageBox(str(e), "Erreur caméra", wx.OK | wx.ICON_ERROR)

    def stop(self):
        """Arrête la caméra."""
        self.timer.Stop()
        self.camera.close()

    def update_frame(self, event):
        """Capture une image et l'affiche dans le panneau."""
        frame = self.camera.read()

        # Si aucune image → ne rien faire
        if frame is None:
            return

        # Convertir BGR → RGB pour wxPython
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        h, w = frame.shape[:2]
        image = wx.Image(w, h, frame.tobytes())

        # Mise à jour de l'affichage
        self.bitmap.SetBitmap(wx.Bitmap(image))
        self.Refresh()

