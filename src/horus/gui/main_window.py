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
        super(MainWindow, self).__init__(parent, title=title, size=(1200, 900))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Titre
        title_text = wx.StaticText(panel, label="Horus RPi5 - Scanner 3D Ciclop (Version IA)")
        font = title_text.GetFont()
        font.PointSize += 4
        font = font.Bold()
        title_text.SetFont(font)
        vbox.Add(title_text, 0, wx.ALL | wx.CENTER, 10)

        # Notebook (onglets)
        notebook = wx.Notebook(panel)

        # Onglet caméra
        cam_tab = wx.Panel(notebook)
        cam_sizer = wx.BoxSizer(wx.VERTICAL)

        self.preview_panel = PreviewPanel(cam_tab)
        cam_sizer.Add(self.preview_panel, 0, wx.EXPAND | wx.ALL, 10)

        self.camera_panel = CameraPanel(cam_tab)
        cam_sizer.Add(self.camera_panel, 1, wx.EXPAND | wx.ALL, 10)

        hbox_cam = wx.BoxSizer(wx.HORIZONTAL)
        btn_start = wx.Button(cam_tab, label="Démarrer caméra")
        btn_stop = wx.Button(cam_tab, label="Arrêter caméra")
        btn_start.Bind(wx.EVT_BUTTON, lambda evt: self.camera_panel.start())
        btn_stop.Bind(wx.EVT_BUTTON, lambda evt: self.camera_panel.stop())
        hbox_cam.Add(btn_start, 0, wx.ALL, 5)
        hbox_cam.Add(btn_stop, 0, wx.ALL, 5)
        cam_sizer.Add(hbox_cam, 0, wx.CENTER)

        cam_tab.SetSizer(cam_sizer)
        notebook.AddPage(cam_tab, "Caméra")

        # Onglet GRBL
        grbl_tab = wx.Panel(notebook)
        grbl_sizer = wx.BoxSizer(wx.VERTICAL)
        self.rotation_panel = RotationPanel(grbl_tab)
        self.grbl_panel = GRBLPanel(grbl_tab)
        grbl_sizer.Add(self.rotation_panel, 0, wx.EXPAND | wx.ALL, 10)
        grbl_sizer.Add(self.grbl_panel, 0, wx.EXPAND | wx.ALL, 10)
        grbl_tab.SetSizer(grbl_sizer)
        notebook.AddPage(grbl_tab, "Moteur / Rotation")

        # Onglet Calibration
        calib_tab = wx.Panel(notebook)
        calib_sizer = wx.BoxSizer(wx.VERTICAL)
        self.calibration_panel = CalibrationPanel(calib_tab)
        calib_sizer.Add(self.calibration_panel, 1, wx.EXPAND | wx.ALL, 10)
        calib_tab.SetSizer(calib_sizer)
        notebook.AddPage(calib_tab, "Calibration")

        # Onglet Scan
        scan_tab = wx.Panel(notebook)
        scan_sizer = wx.BoxSizer(wx.VERTICAL)
        self.scan_panel = ScanPanel(scan_tab)
        scan_sizer.Add(self.scan_panel, 1, wx.EXPAND | wx.ALL, 10)
        scan_tab.SetSizer(scan_sizer)
        notebook.AddPage(scan_tab, "Scan 3D")

        # Onglet IA
        ai_tab = wx.Panel(notebook)
        ai_sizer = wx.BoxSizer(wx.VERTICAL)
        self.ai_panel = AiPanel(ai_tab)
        ai_sizer.Add(self.ai_panel, 1, wx.EXPAND | wx.ALL, 10)
        ai_tab.SetSizer(ai_sizer)
        notebook.AddPage(ai_tab, "IA")

        # Onglet Paramètres
        settings_tab = wx.Panel(notebook)
        settings_sizer = wx.BoxSizer(wx.VERTICAL)
        self.settings_panel = SettingsPanel(settings_tab)
        settings_sizer.Add(self.settings_panel, 1, wx.EXPAND | wx.ALL, 10)
        settings_tab.SetSizer(settings_sizer)
        notebook.AddPage(settings_tab, "Paramètres")

        vbox.Add(notebook, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(vbox)
        self.Centre()
