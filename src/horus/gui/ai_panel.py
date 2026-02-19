import wx

# Ici tu pourras brancher tes vraies fonctions IA
# dans horus/engine/ai.py (à créer)
# ex: from horus.engine.ai import enhance_laser_line, clean_point_cloud, ...

class AiLaserPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="IA Laser : détection et amélioration de la ligne laser"), 0, wx.ALL, 5)
        self.SetSizer(sizer)

class AiPointCloudPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="IA Nuage de points : nettoyage, lissage, interpolation"), 0, wx.ALL, 5)
        self.SetSizer(sizer)

class AiCalibrationPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="IA Calibration : estimation automatique des paramètres"), 0, wx.ALL, 5)
        self.SetSizer(sizer)

class AiCameraAnalyzerPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="IA Caméra : analyse en temps réel, auto-exposition, qualité"), 0, wx.ALL, 5)
        self.SetSizer(sizer)

class AiAssistantPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="Assistant IA : diagnostic, conseils, aide au scan"), 0, wx.ALL, 5)
        self.SetSizer(sizer)

class AiPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        notebook = wx.Notebook(self)

        notebook.AddPage(AiAssistantPanel(notebook), "Assistant")
        notebook.AddPage(AiCameraAnalyzerPanel(notebook), "Caméra IA")
        notebook.AddPage(AiLaserPanel(notebook), "Laser IA")
        notebook.AddPage(AiCalibrationPanel(notebook), "Calibration IA")
        notebook.AddPage(AiPointCloudPanel(notebook), "Nuage IA")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="Module IA Horus RPi5"), 0, wx.ALL, 5)
        sizer.Add(notebook, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)
