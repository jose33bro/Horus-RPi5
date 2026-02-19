import wx
from horus.gui.settings_panel import SettingsPanel
from horus.gui.camera_panel import CameraPanel
from horus.gui.grbl_panel import GRBLPanel
from horus.gui.scan_panel import ScanPanel
from horus.gui.calibration_panel import CalibrationPanel
from horus.gui.preview_panel import PreviewPanel
from horus.gui.rotation_panel import RotationPanel
from horus.gui.ai_panel import AiPanel

class MainWindow(wx.Frame):
    def __init__(self, parent, title="Horus RPi5 IA"):
        super(MainWindow, self).__init__(parent, title=title, size=(1200, 1000))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        title_text = wx.StaticText(panel, label="Horus RPi5 - Scanner 3D Ciclop (Version IA)")
        font = title_text.GetFont()
        font.PointSize += 4
        font = font.Bold()
        title_text.SetFont(font)
        vbox.Add(title_text, 0, wx.ALL | wx.CENTER, 10)

        self.settings_panel = SettingsPanel(panel)
        vbox.Add(self.settings_panel, 0, wx.EXPAND | wx.ALL, 10)

        self.preview_panel = PreviewPanel(panel)
        vbox.Add(self.preview_panel, 0, wx.EXPAND | wx.ALL, 10)

        self.camera_panel = CameraPanel(panel)
        vbox.Add(self.camera_panel, 1, wx.EXPAND | wx.ALL, 10)

        hbox_cam = wx.BoxSizer(wx.HORIZONTAL)
        btn_start = wx.Button(panel, label="Démarrer caméra")
        btn_stop = wx.Button(panel, label="Arrêter caméra")
        btn_start.Bind(wx.EVT_BUTTON, lambda evt: self.camera_panel.start())
        btn_stop.Bind(wx.EVT_BUTTON, lambda evt: self.camera_panel.stop())
        hbox_cam.Add(btn_start, 0, wx.ALL, 5)
        hbox_cam.Add(btn_stop, 0, wx.ALL, 5)
        vbox.Add(hbox_cam, 0, wx.CENTER)

        self.rotation_panel = RotationPanel(panel)
        vbox.Add(self.rotation_panel, 0, wx.EXPAND | wx.ALL, 10)

        self.calibration_panel = CalibrationPanel(panel)
        vbox.Add(self.calibration_panel, 0, wx.EXPAND | wx.ALL, 10)

        self.grbl_panel = GRBLPanel(panel)
        vbox.Add(self.grbl_panel, 0, wx.EXPAND | wx.ALL, 10)

        self.scan_panel = ScanPanel(panel)
        vbox.Add(self.scan_panel, 0, wx.EXPAND | wx.ALL, 10)

        self.ai_panel = AiPanel(panel)
        vbox.Add(self.ai_panel, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(vbox)
        self.Centre()

