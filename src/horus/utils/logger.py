import logging
import logging.handlers
import os

def setup_logger():
    logger = logging.getLogger("HorusRPi5")

    # Empêcher les doublons si déjà configuré
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Dossier logs dans le dossier du projet
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    log_dir = os.path.join(base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "horus.log")

    # Format enrichi
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s"
    )

    # Handler fichier avec rotation
    fh = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=2_000_000,   # 2 MB
        backupCount=5
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # Handler console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

logger = setup_logger()
