import wx
import cv2
from horus.engine.ai_laser import LaserAI
from horus.engine.ai_pointcloud import PointCloudAI
from horus.engine.ai_calibration import CalibrationAI

class AiPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

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

    # LASER IA
    def build_laser(self, parent):
        panel = wx.Panel(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        btn = wx.Button(panel, label="Analyser laser")
        btn.Bind(wx.EVT_BUTTON, self.on_laser)

        self.laser_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        sizer.Add(btn, 0, wx.ALL, 5)
        sizer.Add(self.laser_output, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(sizer)
        return panel

    def on_laser(self, evt):
        self.laser_output.SetValue("Laser IA prêt (modèle TFLite ou OpenCV).")

    # CALIBRATION IA
    def build_calibration(self, parent):
        panel = wx.Panel(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        btn = wx.Button(panel, label="Calibration automatique")
        btn.Bind(wx.EVT_BUTTON, self.on_calibration)

        self.calib_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        sizer.Add(btn, 0, wx.ALL, 5)
        sizer.Add(self.calib_output, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(sizer)
        return panel

    def on_calibration(self, evt):
        self.calib_output.SetValue("Calibration IA prête.")

    # NUAGE IA
    def build_pointcloud(self, parent):
        panel = wx.Panel(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        btn = wx.Button(panel, label="Nettoyer nuage de points")
        btn.Bind(wx.EVT_BUTTON, self.on_pointcloud)

        self.pc_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        sizer.Add(btn, 0, wx.ALL, 5)
        sizer.Add(self.pc_output, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(sizer)
        return panel

    def on_pointcloud(self, evt):
        self.pc_output.SetValue("Nettoyage IA prêt.")

