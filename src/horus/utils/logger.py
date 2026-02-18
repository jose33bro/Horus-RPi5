import logging
import os

def setup_logger():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger("HorusRPi5")
    logger.setLevel(logging.DEBUG)

    # Fichier
    fh = logging.FileHandler("logs/horus.log")
    fh.setLevel(logging.DEBUG)

    # Console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

logger = setup_logger()
