import wx
from horus.engine.grbl_controller import GRBLController

class RotationPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.grbl = GRBLController()

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

        # Ajout au sizer
        for btn in [
            btn_left, btn_right, btn_home,
            btn_laser_left, btn_laser_right, btn_laser_off
        ]:
            sizer.Add(btn, 0, wx.ALL, 5)

        self.SetSizer(sizer)

    def rotate(self, delta_angle):
        """Rotation relative du plateau."""
        try:
            self.grbl.connect()
            self.grbl.rotate_relative(delta_angle)
        except Exception as e:
            wx.MessageBox(str(e), "Erreur GRBL")
        finally:
            self.grbl.disconnect()

    def home(self):
        """Retour à X0."""
        try:
            self.grbl.connect()
            self.grbl.send("G0 X0")
        except Exception as e:
            wx.MessageBox(str(e), "Erreur GRBL")
        finally:
            self.grbl.disconnect()

    def set_laser(self, left=False, right=False):
        """Contrôle des lasers."""
        try:
            self.grbl.connect()
            self.grbl.set_laser(left=left, right=right)
        except Exception as e:
            wx.MessageBox(str(e), "Erreur GRBL")
        finally:
            self.grbl.disconnect()
