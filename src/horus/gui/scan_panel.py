import wx
import threading
from horus.engine.scan import ScanEngine
from horus.utils.calibration_store import CalibrationStore
from horus.utils.logger import logger

class ScanPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.scan_engine = ScanEngine()
        self.store = CalibrationStore()
        self.scanning = False

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Bouton lancer scan
        self.btn_scan = wx.Button(self, label="Lancer un scan complet")
        self.btn_scan.Bind(wx.EVT_BUTTON, self.on_scan)
        vbox.Add(self.btn_scan, 0, wx.ALL, 10)

        # Bouton stop
        self.btn_stop = wx.Button(self, label="Arrêter le scan")
        self.btn_stop.Disable()
        self.btn_stop.Bind(wx.EVT_BUTTON, self.on_stop)
        vbox.Add(self.btn_stop, 0, wx.ALL, 10)

        # Barre de progression
        self.progress = wx.Gauge(self, range=360)
        vbox.Add(self.progress, 0, wx.EXPAND | wx.ALL, 10)

        # Zone de log
        self.log = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.log, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(vbox)

    def on_scan(self, event):
        # Vérification calibration
        if self.store.left_plane is None or self.store.right_plane is None:
            wx.MessageBox("Calibration laser manquante !", "Erreur")
            return

        self.log.AppendText("Début du scan...\n")
        logger.info("Début du scan")

        self.btn_scan.Disable()
        self.btn_stop.Enable()
        self.scanning = True

        # Thread pour ne pas bloquer la GUI
        thread = threading.Thread(target=self.run_scan_thread)
        thread.start()

    def run_scan_thread(self):
        try:
            for angle, status in self.scan_engine.run_scan_yield():
                wx.CallAfter(self.progress.SetValue, angle)
                wx.CallAfter(self.log.AppendText, f"{status}\n")

                if not self.scanning:
                    wx.CallAfter(self.log.AppendText, "Scan interrompu.\n")
                    return

            wx.CallAfter(self.log.AppendText, "Scan terminé !\n")
            wx.CallAfter(wx.MessageBox, "Scan terminé ! Fichier : scan.ply", "Info")

        except Exception as e:
            wx.CallAfter(self.log.AppendText, f"Erreur : {e}\n")
            wx.CallAfter(wx.MessageBox, str(e), "Erreur")

        finally:
            wx.CallAfter(self.btn_scan.Enable)
            wx.CallAfter(self.btn_stop.Disable)
            self.scanning = False

    def on_stop(self, event):
        self.scanning = False
        self.btn_stop.Disable()
        self.log.AppendText("Arrêt demandé...\n")
