import wx
from horus.utils.config import Config


class SettingsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.cfg = Config()

        vbox = wx.BoxSizer(wx.VERTICAL)

        # -------------------------
        # MODE DE SCAN
        # -------------------------
        vbox.Add(wx.StaticText(self, label="Mode de scan"), 0, wx.ALL, 5)

        modes = ["fast", "high_quality"]
        self.choice_mode = wx.Choice(self, choices=modes)

        # Charger la valeur actuelle
        current = self.cfg.get("scan_mode", "fast")
        if current in modes:
            self.choice_mode.SetStringSelection(current)
        else:
            self.choice_mode.SetSelection(0)

        vbox.Add(self.choice_mode, 0, wx.ALL, 5)

        # -------------------------
        # ANGLE PAR PAS
        # -------------------------
        vbox.Add(wx.StaticText(self, label="Angle par pas (°)"), 0, wx.ALL, 5)

        self.spin_angle = wx.SpinCtrl(self, min=1, max=45)
        self.spin_angle.SetValue(self.cfg.get("step_angle", 5))

        vbox.Add(self.spin_angle, 0, wx.ALL, 5)

        # -------------------------
        # RÉPERTOIRE DE SORTIE
        # -------------------------
        vbox.Add(wx.StaticText(self, label="Dossier de sortie"), 0, wx.ALL, 5)

        self.txt_output = wx.TextCtrl(self)
        self.txt_output.SetValue(self.cfg.get("output_dir", "./"))

        vbox.Add(self.txt_output, 0, wx.EXPAND | wx.ALL, 5)

        # -------------------------
        # BOUTON APPLIQUER
        # -------------------------
        btn_apply = wx.Button(self, label="Enregistrer les paramètres")
        btn_apply.Bind(wx.EVT_BUTTON, self.on_apply)

        vbox.Add(btn_apply, 0, wx.ALL, 10)

        self.SetSizer(vbox)

    def on_apply(self, event):
        mode = self.choice_mode.GetStringSelection()
        angle = self.spin_angle.GetValue()
        output = self.txt_output.GetValue()

        # Sauvegarde dans config.json
        self.cfg.set("scan_mode", mode)
        self.cfg.set("step_angle", angle)
        self.cfg.set("output_dir", output)
        self.cfg.save()

        wx.MessageBox("Paramètres enregistrés.", "OK")
