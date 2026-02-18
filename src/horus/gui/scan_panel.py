import wx
from horus.engine.camera import Camera
from horus.engine.profile_extractor import ProfileExtractor
from horus.engine.reconstruction import Reconstruction3D
from horus.engine.grbl_controller import GRBLController
from horus.utils.logger import logger
    logger.info("Début du scan")
    logger.info(f"Étape {step}/{steps}")
    logger.info("Scan terminé, export PLY")

class ScanPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.camera = Camera()
        self.extractor = ProfileExtractor()
        self.reconstruction = Reconstruction3D()
        self.grbl = GRBLController()

        vbox = wx.BoxSizer(wx.VERTICAL)

        btn_scan = wx.Button(self, label="Lancer un scan complet")
        btn_scan.Bind(wx.EVT_BUTTON, self.on_scan)

        vbox.Add(btn_scan, 0, wx.ALL, 10)

        self.SetSizer(vbox)

    def on_scan(self, event):
        wx.MessageBox("Début du scan", "Info")

        self.grbl.connect()
        self.camera.open()

        angle = 0

from horus.utils.config import Config

cfg = Config()
steps = cfg.get("scan.steps")
step_angle = cfg.get("grbl.step_angle")

for step in range(steps):
    ...
    angle += step_angle
 
            frame = self.camera.read()
            profile = self.extractor.extract_profile(frame)
            self.reconstruction.add_profile(profile, angle)

            angle += 1.8
            self.grbl.rotate_step()

        self.camera.close()
        self.grbl.disconnect()

        self.reconstruction.export_ply("scan.ply")
        self.reconstruction.export_obj("scan.obj")

        wx.MessageBox("Scan terminé ! Fichier : scan.ply", "OK")
