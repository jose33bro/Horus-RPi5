import wx
from horus.engine.grbl_controller import GRBLController

class RotationPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.grbl = GRBLController()
        self.connected = False
        self.busy = False

        sizer = wx.BoxSizer(wx.VERTICAL)

        # Boutons rotation
        btn_left = wx.Button(self, label="⟲ Rotation -5°")
        btn_right = wx.Button(self, label="⟳ Rotation +5°")
        btn_home = wx.Button(self, label="Home (X0)")

        btn_left.Bind(wx.EVT_BUTTON, lambda evt: self.rotate(-5))
        btn_right.Bind(wx.EVT_BUTTON, lambda evt: self.rotate(5))
        btn_home.Bind(wx.EVT_BUTTON, lambda evt: self.home())

        # Boutons laser
        btn_laser_left = wx.Button(self, label="Laser gauche")
        btn_laser_right = wx.Button(self, label="Laser droit")
        btn_laser_off = wx.Button(self, label="Laser OFF")

        btn_laser_left.Bind(wx.EVT_BUTTON, lambda evt: self.set_laser(left=True))
        btn_laser_right.Bind(wx.EVT_BUTTON, lambda evt: self.set_laser(right=True))
        btn_laser_off.Bind(wx.EVT_BUTTON, lambda evt: self.set_laser())

        # Label d'état
        self.status = wx.StaticText(self, label="GRBL : déconnecté")

        for item in [
            btn_left, btn_right, btn_home,
            btn_laser_left, btn_laser_right, btn_laser_off,
            self.status
        ]:
            sizer.Add(item, 0, wx.ALL, 5)

        self.SetSizer(sizer)

        # Connexion persistante
        self.connect()

    def connect(self):
        if self.connected:
            return
        try:
            self.grbl.connect()
            self.connected = True
            self.status.SetLabel("GRBL : connecté")
        except Exception as e:
            wx.MessageBox(str(e), "Erreur GRBL")

    def rotate(self, delta_angle):
        if not self.connected or self.busy:
            return

        self.busy = True
        try:
            self.grbl.rotate_relative(delta_angle)
        except Exception as e:
            wx.MessageBox(str(e), "Erreur GRBL")
        finally:
            self.busy = False

    def home(self):
        if not self.connected or self.busy:
            return

        self.busy = True
        try:
            self.grbl.send("G0 X0")
        except Exception as e:
            wx.MessageBox(str(e), "Erreur GRBL")
        finally:
            self.busy = False

    def set_laser(self, left=False, right=False):
        if not self.connected or self.busy:
            return

        try:
            self.grbl.set_laser(left=left, right=right)
        except Exception as e:
            wx.MessageBox(str(e), "Erreur GRBL")
