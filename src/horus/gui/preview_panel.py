import wx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

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

    def load_ply(self, filename):
        """Charge un fichier PLY simple (x y z)"""
        points = []
        with open(filename, "r") as f:
            header = True
            for line in f:
                if header:
                    if line.strip() == "end_header":
                        header = False
                    continue
                parts = line.strip().split()
                if len(parts) >= 3:
                    x, y, z = map(float, parts[:3])
                    points.append([x, y, z])
        return np.array(points)

    def on_preview(self, event):
        try:
            points = self.load_ply("scan.ply")
        except Exception as e:
            wx.MessageBox(f"Impossible de charger scan.ply : {e}", "Erreur")
            return

        if points.size == 0:
            wx.MessageBox("Le fichier scan.ply est vide.", "Erreur")
            return

        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(points[:,0], points[:,1], points[:,2], s=1)

        fig.savefig("preview.png")
        plt.close(fig)

        img = wx.Image("preview.png", wx.BITMAP_TYPE_PNG)
        self.bitmap.SetBitmap(wx.Bitmap(img))
