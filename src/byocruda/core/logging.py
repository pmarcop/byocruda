import sys
from loguru import logger
from byocruda.core.config import settings

def setup_logging():
    """Configure logging for the application."""
    # Remove default handler
    logger.remove()

    # Configure console logging
    logger.add(
        sys.stderr,
        format=settings.logging.format,
        level=settings.logging.level,
        colorize=True,
    )

    # Configure file logging
    logger.add(
        settings.logging.file_path,
        format=settings.logging.format,
        level=settings.logging.level,
        rotation=settings.logging.rotation,
        retention=settings.logging.retention,
    )

    # You can add more custom configurations here if needed

    return logger

# Create a global logger instance
log = setup_logging()
