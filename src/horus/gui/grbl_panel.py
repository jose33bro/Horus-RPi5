import wx
from horus.engine.grbl_controller import GRBLController

class GRBLPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.grbl = GRBLController()
        self.connected = False
        self.busy = False

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Connexion
        btn_connect = wx.Button(self, label="Connecter GRBL")
        btn_disconnect = wx.Button(self, label="Déconnecter")

        btn_connect.Bind(wx.EVT_BUTTON, self.on_connect)
        btn_disconnect.Bind(wx.EVT_BUTTON, self.on_disconnect)

        vbox.Add(btn_connect, 0, wx.ALL, 5)
        vbox.Add(btn_disconnect, 0, wx.ALL, 5)

        # Champ G-code manuel
        hbox_cmd = wx.BoxSizer(wx.HORIZONTAL)
        self.cmd_input = wx.TextCtrl(self)
        btn_send = wx.Button(self, label="Envoyer G-code")
        btn_send.Bind(wx.EVT_BUTTON, self.on_send_gcode)

        hbox_cmd.Add(self.cmd_input, 1, wx.ALL, 5)
        hbox_cmd.Add(btn_send, 0, wx.ALL, 5)

        vbox.Add(hbox_cmd, 0, wx.EXPAND)

        # Boutons utiles
        btn_unlock = wx.Button(self, label="Unlock ($X)")
        btn_reset = wx.Button(self, label="Reset (CTRL-X)")
        btn_status = wx.Button(self, label="Lire statut ($G)")

        btn_unlock.Bind(wx.EVT_BUTTON, lambda evt: self.send("$X"))
        btn_reset.Bind(wx.EVT_BUTTON, lambda evt: self.send("\x18"))
        btn_status.Bind(wx.EVT_BUTTON, lambda evt: self.send("$G"))

        for b in [btn_unlock, btn_reset, btn_status]:
            vbox.Add(b, 0, wx.ALL, 5)

        # Zone de log GRBL
        self.log = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.log, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(vbox)

    def on_connect(self, event):
        if self.connected:
            return
        try:
            self.grbl.connect()
            self.connected = True
            self.log.AppendText("GRBL connecté\n")
        except Exception as e:
            wx.MessageBox(str(e), "Erreur GRBL")

    def on_disconnect(self, event):
        if not self.connected:
            return
        self.grbl.disconnect()
        self.connected = False
        self.log.AppendText("GRBL déconnecté\n")

    def send(self, cmd):
        if not self.connected:
            wx.MessageBox("GRBL non connecté", "Erreur")
            return
        try:
            resp = self.grbl.send(cmd)
            self.log.AppendText(f"> {cmd}\n{resp}\n")
        except Exception as e:
            wx.MessageBox(str(e), "Erreur GRBL")

    def on_send_gcode(self, event):
        cmd = self.cmd_input.GetValue().strip()
        if cmd:
            self.send(cmd)
