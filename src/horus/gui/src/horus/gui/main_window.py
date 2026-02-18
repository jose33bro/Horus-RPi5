import wx
from horus.gui.camera_panel import CameraPanel

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

        # Panneau caméra
        self.camera_panel = CameraPanel(panel)
        vbox.Add(self.camera_panel, 1, wx.EXPAND | wx.ALL, 10)

        # Boutons
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_start = wx.Button(panel, label="Démarrer caméra")
        btn_stop = wx.Button(panel, label="Arrêter caméra")

        btn_start.Bind(wx.EVT_BUTTON, lambda evt: self.camera_panel.start())
        btn_stop.Bind(wx.EVT_BUTTON, lambda evt: self.camera_panel.stop())

        hbox.Add(btn_start, 0, wx.ALL, 5)
        hbox.Add(btn_stop, 0, wx.ALL, 5)

        vbox.Add(hbox, 0, wx.CENTER)

        panel.SetSizer(vbox)
        self.Centre()
