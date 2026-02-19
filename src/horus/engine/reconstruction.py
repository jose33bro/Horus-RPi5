import math

class Reconstruction3D:
    def __init__(self, left_plane=None, right_plane=None):
        self.left_plane = left_plane
        self.right_plane = right_plane
        self.points = []

    def add_profile(self, profile_points, angle_deg):
        """
        Convertit un profil 2D en points 3D.
        angle_deg = angle du plateau au moment de la capture.
        """
        angle = math.radians(angle_deg)

        for x, y in profile_points:
            # Conversion simple : rayon = x, hauteur = y
            r = x
            h = y

            X = r * math.cos(angle)
            Y = r * math.sin(angle)
            Z = h

            self.points.append((X, Y, Z))

    def export_ply(self, filename="scan.ply"):
        """
        Exporte les points au format PLY.
        """
        with open(filename, "w") as f:
            f.write("ply\n")
            f.write("format ascii 1.0\n")
            f.write(f"element vertex {len(self.points)}\n")
            f.write("property float x\n")
            f.write("property float y\n")
            f.write("property float z\n")
            f.write("end_header\n")

            for p in self.points:
                f.write(f"{p[0]} {p[1]} {p[2]}\n")

    def export_obj(self, filename="scan.obj"):
        """
        Exporte les points au format OBJ.
        """
        with open(filename, "w") as f:
            for p in self.points:
                f.write(f"v {p[0]} {p[1]} {p[2]}\n")
