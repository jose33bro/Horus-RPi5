import wx
from horus.gui.main_window import MainWindow

class HorusApp(wx.App):
    def OnInit(self):
        self.frame = MainWindow(None, title="Horus RPi5 Edition")
        self.frame.Show()
        return True

def main():
    app = HorusApp(False)
    app.MainLoop()

if __name__ == "__main__":
    main()
