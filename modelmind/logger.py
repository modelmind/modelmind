import logging

from modelmind.config import settings

log = logging.getLogger(settings.logging.logger_name)

log.setLevel(settings.logging.level.value.upper())
