import wx
import cv2
import numpy as np
from horus.engine.camera import Camera

class CameraPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.camera = Camera()
        self.running = False

        # Timer pour rafraîchir l'image
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_frame, self.timer)

        # Zone d'affichage
        self.bitmap = wx.StaticBitmap(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.bitmap, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

        # Pour éviter les fuites mémoire
        self.current_bitmap = None

    def start(self):
        """Démarre la caméra et le rafraîchissement."""
        if self.running:
            return

        try:
            self.camera.open()
            self.running = True
            self.timer.Start(30)  # ~33 FPS
        except Exception as e:
            wx.MessageBox(str(e), "Erreur caméra", wx.OK | wx.ICON_ERROR)

    def stop(self):
        """Arrête la caméra."""
        if not self.running:
            return

        self.running = False
        self.timer.Stop()
        self.camera.close()

    def update_frame(self, event):
        """Capture une image et l'affiche dans le panneau."""
        frame = self.camera.read()

        if frame is None:
            return

        # Convertir BGR → RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Redimensionner à la taille du panel
        panel_w, panel_h = self.GetSize()
        frame = cv2.resize(frame, (panel_w, panel_h))

        # Convertir en wx.Image
        h, w = frame.shape[:2]
        image = wx.Image(w, h, frame.tobytes())

        # Convertir en bitmap (sans fuite mémoire)
        bmp = wx.Bitmap(image)

        # Mise à jour
        self.bitmap.SetBitmap(bmp)
        self.current_bitmap = bmp  # éviter le garbage collector
        self.Refresh()
