import wx
import cv2
import numpy as np

from horus.engine.camera import Camera
from horus.engine.ai_laser import LaserAI
from horus.engine.ai_pointcloud import PointCloudAI
from horus.engine.ai_calibration import CalibrationAI


class AiPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.camera = Camera()
        self.laser_ai = LaserAI()
        self.pc_ai = PointCloudAI()
        self.calib_ai = CalibrationAI()

        notebook = wx.Notebook(self)
        notebook.AddPage(self.build_laser(notebook), "Laser IA")
        notebook.AddPage(self.build_calibration(notebook), "Calibration IA")
        notebook.AddPage(self.build_pointcloud(notebook), "Nuage IA")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="Module IA Horus RPi5"), 0, wx.ALL, 5)
        sizer.Add(notebook, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

    # -------------------------------
    # LASER IA
    # -------------------------------
    def build_laser(self, parent):
        panel = wx.Panel(parent)
        vbox = wx.BoxSizer(wx.VERTICAL)

        btn = wx.Button(panel, label="Analyser laser (capture caméra)")
        btn.Bind(wx.EVT_BUTTON, self.on_laser)

        self.laser_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.laser_bitmap = wx.StaticBitmap(panel)

        vbox.Add(btn, 0, wx.ALL, 5)
        vbox.Add(self.laser_output, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.laser_bitmap, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(vbox)
        return panel

    def on_laser(self, evt):
        try:
            self.camera.open()
            frame = self.camera.read()
            self.camera.close()

            if frame is None:
                self.laser_output.SetValue("Erreur : impossible de capturer une image.")
                return

            mask = self.laser_ai.detect(frame)
            self.laser_output.SetValue("Laser détecté.\n")

            overlay = frame.copy()
            overlay[mask > 0] = (0, 255, 0)

            rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
            h, w = rgb.shape[:2]
            img = wx.Image(w, h, rgb.tobytes())
            self.laser_bitmap.SetBitmap(wx.Bitmap(img))

        except Exception as e:
            self.laser_output.SetValue(f"Erreur IA : {e}")

    # -------------------------------
    # CALIBRATION IA
    # -------------------------------
    def build_calibration(self, parent):
        panel = wx.Panel(parent)
        vbox = wx.BoxSizer(wx.VERTICAL)

        btn = wx.Button(panel, label="Estimer calibration IA")
        btn.Bind(wx.EVT_BUTTON, self.on_calibration)

        self.calib_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        vbox.Add(btn, 0, wx.ALL, 5)
        vbox.Add(self.calib_output, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(vbox)
        return panel

    def on_calibration(self, evt):
        try:
            self.camera.open()
            frame = self.camera.read()
            self.camera.close()

            if frame is None:
                self.calib_output.SetValue("Erreur : impossible de capturer une image.")
                return

            calib = self.calib_ai.estimate(frame)
            self.calib_output.SetValue(f"Calibration IA estimée :\n{calib}")

        except Exception as e:
            self.calib_output.SetValue(f"Erreur IA : {e}")

    # -------------------------------
    # NUAGE IA
    # -------------------------------
    def build_pointcloud(self, parent):
        panel = wx.Panel(parent)
        vbox = wx.BoxSizer(wx.VERTICAL)

        btn = wx.Button(panel, label="Nettoyer nuage de points (scan.ply)")
        btn.Bind(wx.EVT_BUTTON, self.on_pointcloud)

        self.pc_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        vbox.Add(btn, 0, wx.ALL, 5)
        vbox.Add(self.pc_output, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(vbox)
        return panel

    def on_pointcloud(self, evt):
        try:
            points = np.loadtxt("scan.ply", skiprows=10)
            cleaned = self.pc_ai.clean(points)

            np.savetxt("scan_cleaned.ply", cleaned)
            self.pc_output.SetValue("Nuage nettoyé → scan_cleaned.ply")

        except Exception as e:
            self.pc_output.SetValue(f"Erreur IA : {e}")
