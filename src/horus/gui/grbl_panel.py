import wx
from horus.engine.grbl_controller import GRBLController

class GRBLPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.grbl = GRBLController()

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Boutons connexion
        btn_connect = wx.Button(self, label="Connecter GRBL")
        btn_disconnect = wx.Button(self, label="Déconnecter")

        btn_connect.Bind(wx.EVT_BUTTON, self.on_connect)
        btn_disconnect.Bind(wx.EVT_BUTTON, self.on_disconnect)

        vbox.Add(btn_connect, 0, wx.ALL, 5)
        vbox.Add(btn_disconnect, 0, wx.ALL, 5)

        # Rotation
        btn_rotate = wx.Button(self, label="Rotation +1.8°")
        btn_rotate.Bind(wx.EVT_BUTTON, self.on_rotate)
        vbox.Add(btn_rotate, 0, wx.ALL, 5)

        # Lasers
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_laser_left = wx.Button(self, label="Laser gauche")
        btn_laser_right = wx.Button(self, label="Laser droit")
        btn_laser_off = wx.Button(self, label="Lasers OFF")

        btn_laser_left.Bind(wx.EVT_BUTTON, lambda evt: self.on_laser(left=True))
        btn_laser_right.Bind(wx.EVT_BUTTON, lambda evt: self.on_laser(right=True))
        btn_laser_off.Bind(wx.EVT_BUTTON, lambda evt: self.on_laser())

        hbox.Add(btn_laser_left, 0, wx.ALL, 5)
        hbox.Add(btn_laser_right, 0, wx.ALL, 5)
        hbox.Add(btn_laser_off, 0, wx.ALL, 5)

        vbox.Add(hbox, 0, wx.CENTER)

        self.SetSizer(vbox)

    def on_connect(self, event):
        try:
            self.grbl.connect()
            wx.MessageBox("GRBL connecté", "OK")
        except Exception as e:
            wx.MessageBox(str(e), "Erreur", wx.OK | wx.ICON_ERROR)

    def on_disconnect(self, event):
        self.grbl.disconnect()
        wx.MessageBox("Déconnecté", "OK")

    def on_rotate(self, event):
        self.grbl.rotate_step()

    def on_laser(self, left=False, right=False):
        self.grbl.set_laser(left=left, right=right)
