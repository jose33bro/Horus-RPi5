import wx
import sys
from horus.gui.main_window import MainWindow
from horus.utils.logger import logger

class HorusApp(wx.App):
    def OnInit(self):
        logger.info("Démarrage de Horus RPi5 Edition")

        try:
            self.frame = MainWindow(None, title="Horus RPi5 Edition")
            self.frame.Show()
        except Exception as e:
            logger.error(f"Erreur lors du lancement de la fenêtre principale : {e}")
            raise

        return True

def main():
    try:
        app = HorusApp(False)
        app.MainLoop()
    except Exception as e:
        logger.critical(f"Erreur critique dans l'application : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
