from loguru import logger

def setup_logger():
    """Konfiguriert den Logger."""
    logger.add("pedestrian_communication.log", rotation="1 MB", level="DEBUG")
    return logger