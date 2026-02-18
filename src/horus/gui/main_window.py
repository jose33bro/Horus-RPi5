import wx

class MainWindow(wx.Frame):
    def __init__(self, parent, title="Horus RPi5"):
        super(MainWindow, self).__init__(parent, title=title, size=(1024, 768))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        title_text = wx.StaticText(panel, label="Horus RPi5 - Scanner 3D Ciclop")
        font = title_text.GetFont()
        font.PointSize += 4
        font = font.Bold()
        title_text.SetFont(font)

        vbox.Add(title_text, 0, wx.ALL | wx.CENTER, 10)

        panel.SetSizer(vbox)
        self.Centre()
