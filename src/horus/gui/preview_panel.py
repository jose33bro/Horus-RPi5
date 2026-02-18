import wx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from horus.engine.reconstruction import Reconstruction3D

class PreviewPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        btn = wx.Button(self, label="Afficher le nuage de points")
        btn.Bind(wx.EVT_BUTTON, self.on_preview)

        self.bitmap = wx.StaticBitmap(self)

        vbox.Add(btn, 0, wx.ALL, 5)
        vbox.Add(self.bitmap, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(vbox)

    def on_preview(self, event):
        recon = Reconstruction3D()
        recon.load_from_ply("scan.ply")  # à implémenter si tu veux

        points = np.array(recon.points)

        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(points[:,0], points[:,1], points[:,2], s=1)

        fig.savefig("preview.png")
        plt.close(fig)

        img = wx.Image("preview.png", wx.BITMAP_TYPE_PNG)
        self.bitmap.SetBitmap(wx.Bitmap(img))
