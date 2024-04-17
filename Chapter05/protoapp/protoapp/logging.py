import logging
from logging.handlers import TimedRotatingFileHandler

from uvicorn.logging import ColourizedFormatter

client_logger = logging.getLogger("client.logger")
client_logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()

console_formatter = ColourizedFormatter(
    "%(levelprefix)s CLIENT CALL - %(message)s",
    use_colors=True,
)
console_handler.setFormatter(console_formatter)
client_logger.addHandler(console_handler)

file_handler = TimedRotatingFileHandler("app.log")

file_formatter = logging.Formatter(
    "time %(asctime)s, %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

file_handler.setFormatter(file_formatter)
client_logger.addHandler(file_handler)
