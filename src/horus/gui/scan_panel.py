import wx
from horus.engine.scan import ScanEngine
from horus.utils.logger import logger

class ScanPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.scan_engine = ScanEngine()

        vbox = wx.BoxSizer(wx.VERTICAL)

        btn_scan = wx.Button(self, label="Lancer un scan complet")
        btn_scan.Bind(wx.EVT_BUTTON, self.on_scan)

        vbox.Add(btn_scan, 0, wx.ALL, 10)

        self.SetSizer(vbox)

    def on_scan(self, event):
        wx.MessageBox("Début du scan", "Info")
        logger.info("Début du scan")

        self.scan_engine.run_scan()

        wx.MessageBox("Scan terminé ! Fichier : scan.ply", "Info")
        logger.info("Scan terminé")
