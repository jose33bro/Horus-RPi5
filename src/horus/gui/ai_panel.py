import wx
from horus.engine import ai

class AiPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        notebook = wx.Notebook(self)

        notebook.AddPage(self.build_assistant(notebook), "Assistant IA")
        notebook.AddPage(self.build_camera(notebook), "Caméra IA")
        notebook.AddPage(self.build_laser(notebook), "Laser IA")
        notebook.AddPage(self.build_calibration(notebook), "Calibration IA")
        notebook.AddPage(self.build_pointcloud(notebook), "Nuage IA")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="Module IA Horus RPi5"), 0, wx.ALL, 5)
        sizer.Add(notebook, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

    # Onglet 1 — Assistant IA
    def build_assistant(self, parent):
        panel = wx.Panel(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.assistant_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.assistant_input = wx.TextCtrl(panel)

        btn = wx.Button(panel, label="Envoyer")
        btn.Bind(wx.EVT_BUTTON, self.on_assistant)

        sizer.Add(wx.StaticText(panel, label="Assistant IA"), 0, wx.ALL, 5)
        sizer.Add(self.assistant_output, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.assistant_input, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(btn, 0, wx.ALL, 5)

        panel.SetSizer(sizer)
        return panel

    def on_assistant(self, evt):
        question = self.assistant_input.GetValue()
        result = ai.ai_assistant({"system": "OK"}, question)
        self.assistant_output.SetValue(str(result))

    # Onglet 2 — Analyse caméra
    def build_camera(self, parent):
        panel = wx.Panel(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel, label="Analyse IA de la caméra"), 0, wx.ALL, 5)
        panel.SetSizer(sizer)
        return panel

    # Onglet 3 — Laser IA
    def build_laser(self, parent):
        panel = wx.Panel(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel, label="Détection IA du laser"), 0, wx.ALL, 5)
        panel.SetSizer(sizer)
        return panel

    # Onglet 4 — Calibration IA
    def build_calibration(self, parent):
        panel = wx.Panel(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel, label="Calibration automatique IA"), 0, wx.ALL, 5)
        panel.SetSizer(sizer)
        return panel

    # Onglet 5 — Nuage IA
    def build_pointcloud(self, parent):
        panel = wx.Panel(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel, label="Nettoyage IA du nuage de points"), 0, wx.ALL, 5)
        panel.SetSizer(sizer)
        return panel
