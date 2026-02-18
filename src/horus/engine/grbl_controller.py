import serial
import time

class GRBLController:
from horus.utils.config import Config

class GRBLController:
    def __init__(self):
        cfg = Config()
        self.port = cfg.get("grbl.port")
        self.baudrate = cfg.get("grbl.baudrate")
        self.step_angle = cfg.get("grbl.step_angle")
        self.timeout = 1

        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # Laisser GRBL démarrer
            self.flush()
        except Exception as e:
            raise RuntimeError(f"Impossible de se connecter à GRBL : {e}")

    def flush(self):
        if self.ser:
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()

    def send(self, command):
        if not self.ser:
            raise RuntimeError("GRBL n'est pas connecté")

        cmd = (command + "\n").encode()
        self.ser.write(cmd)
        self.ser.flush()

        response = self.ser.readline().decode().strip()
        return response

    def rotate_step(self, angle=1.8):
        """Rotation du plateau (axe A)"""
        return self.send(f"G0 A{angle}")

    def set_laser(self, left=False, right=False):
        """Contrôle des lasers via M3/M5 ou sorties GRBL modifiées"""
        if left and right:
            return self.send("M3 S255")  # les deux lasers
        elif left:
            return self.send("M3 S128")  # laser gauche
        elif right:
            return self.send("M3 S64")   # laser droit
        else:
            return self.send("M5")       # lasers off

    def disconnect(self):
        if self.ser:
            self.ser.close()
            self.ser = None
