import wx
import numpy as np
import matplotlib
matplotlib.use("WXAgg")
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

class PreviewPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        btn = wx.Button(self, label="Afficher le nuage de points")
        btn.Bind(wx.EVT_BUTTON, self.on_preview)
        vbox.Add(btn, 0, wx.ALL, 5)

        # Figure matplotlib interactive
        self.fig = Figure(figsize=(5, 5))
        self.ax = self.fig.add_subplot(111, projection="3d")

        self.canvas = FigureCanvas(self, -1, self.fig)
        vbox.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(vbox)

    def load_ply(self, filename):
        """Charge un fichier PLY simple (x y z)"""
        points = []
        try:
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
        except Exception as e:
            raise RuntimeError(f"Erreur lecture PLY : {e}")

        return np.array(points)

    def on_preview(self, event):
        try:
            points = self.load_ply("scan.ply")
        except Exception as e:
            wx.MessageBox(str(e), "Erreur")
            return

        if points.size == 0:
            wx.MessageBox("Le fichier scan.ply est vide.", "Erreur")
            return

        # Clear previous plot
        self.ax.clear()

        # Scatter 3D interactif
        self.ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=1)

        self.ax.set_title("Nuage de points 3D")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        self.canvas.draw()
