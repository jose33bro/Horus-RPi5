import serial
import time
from horus.utils.config import Config
from horus.utils.logger import logger

class GRBLController:
    def __init__(self):
        cfg = Config()

        self.port = cfg.get("grbl.port", "/dev/ttyUSB0")
        self.baudrate = cfg.get("grbl.baudrate", 115200)
        self.step_angle = cfg.get("grbl.step_angle", 1.8)
        self.timeout = cfg.get("grbl.timeout", 1)

        self.ser = None

    def connect(self):
        logger.info(f"Connexion à GRBL sur {self.port} ({self.baudrate} bauds)")

        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # GRBL démarre
            self.flush()

            # Déverrouiller GRBL si nécessaire
            self.send("$X")

        except Exception as e:
            logger.error(f"Erreur connexion GRBL : {e}")
            raise RuntimeError(f"Impossible de se connecter à GRBL : {e}")

    def flush(self):
        if self.ser:
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()

    def send(self, command):
        if not self.ser:
            raise RuntimeError("GRBL n'est pas connecté")

        logger.debug(f"Commande envoyée : {command}")

        cmd = (command + "\n").encode()
        self.ser.write(cmd)
        self.ser.flush()

        response = self.ser.readline().decode().strip()
        logger.debug(f"Réponse GRBL : {response}")

        if response.startswith("error"):
            logger.error(f"Erreur GRBL : {response}")
            raise RuntimeError(f"Erreur GRBL : {response}")

        return response

    def rotate_step(self):
        """Rotation du plateau (axe A)"""
        return self.send(f"G0 A{self.step_angle}")

    def rotate_relative(self, delta_angle):
        """Rotation relative en degrés"""
        return self.send(f"G91\nG0 A{delta_angle}\nG90")

    def set_laser(self, left=False, right=False):
        """Contrôle des lasers via M3/M5"""
        if left and right:
            return self.send("M3 S255")
        elif left:
            return self.send("M3 S128")
        elif right:
            return self.send("M3 S64")
        else:
            return self.send("M5")

    def disconnect(self):
        if self.ser:
            logger.info("Déconnexion GRBL")
            self.ser.close()
            self.ser = None
