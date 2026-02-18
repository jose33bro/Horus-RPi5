import wx
from horus.gui.settings_panel import SettingsPanel
from horus.gui.camera_panel import CameraPanel
from horus.gui.grbl_panel import GRBLPanel
from horus.gui.scan_panel import ScanPanel
from horus.gui.calibration_panel import CalibrationPanel
from horus.gui.preview_panel import PreviewPanel

class MainWindow(wx.Frame):
    def __init__(self, parent, title="Horus RPi5"):
        super(MainWindow, self).__init__(parent, title=title, size=(1024, 768))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Titre
        title_text = wx.StaticText(panel, label="Horus RPi5 - Scanner 3D Ciclop")
        font = title_text.GetFont()
        font.PointSize += 4
        font = font.Bold()
        title_text.SetFont(font)
        vbox.Add(title_text, 0, wx.ALL | wx.CENTER, 10)
        
        self.settings_panel = SettingsPanel(panel)
        vbox.Add(self.settings_panel, 0, wx.EXPAND | wx.ALL, 10)

        self.preview_panel = PreviewPanel(panel)
        vbox.Add(self.preview_panel, 0, wx.EXPAND | wx.ALL, 10)

        # Panneau caméra
        self.camera_panel = CameraPanel(panel)
        vbox.Add(self.camera_panel, 1, wx.EXPAND | wx.ALL, 10)

        self.calibration_panel = CalibrationPanel(panel)
        vbox.Add(self.calibration_panel, 0, wx.EXPAND | wx.ALL, 10)

        # Panneau GRBL (plateau + lasers)
        self.grbl_panel = GRBLPanel(panel)
        vbox.Add(self.grbl_panel, 0, wx.EXPAND | wx.ALL, 10)
        
        self.scan_panel = ScanPanel(panel)
        vbox.Add(self.scan_panel, 0, wx.EXPAND | wx.ALL, 10)
        
        panel.SetSizer(vbox)
        self.Centre()
