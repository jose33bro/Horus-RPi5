import wx
from horus.utils.config import Config

class SettingsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.cfg = Config()

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Mode de scan
        modes = ["fast", "high_quality"]
        self.choice_mode = wx.Choice(self, choices=modes)
        self.choice_mode.SetSelection(0)

        btn_apply = wx.Button(self, label="Appliquer le mode")
        btn_apply.Bind(wx.EVT_BUTTON, self.on_apply)

        vbox.Add(wx.StaticText(self, label="Mode de scan"), 0, wx.ALL, 5)
        vbox.Add(self.choice_mode, 0, wx.ALL, 5)
        vbox.Add(btn_apply, 0, wx.ALL, 5)

        self.SetSizer(vbox)

    def on_apply(self, event):
        mode = self.choice_mode.GetStringSelection()
        wx.MessageBox(f"Mode '{mode}' appliqué (à implémenter)", "Info")
