import logging.config
import pprint
from datetime import datetime

logger = logging.getLogger("arcbest_api")
logging_config = {
        "version"                 : 1,
        "disable_existing_loggers": False,
        "formatters"              : {"standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
                                     "detailed": {
                                             "format" : "%(asctime)s [%(levelname)s|%(module)s|L%(lineno)d] %(name)s: %(message)s",
                                             "datefmt": "%Y-%m-%dT%H:%M:%S%z"}
                                     },

        "handlers"                : {
                "stdout": {
                        "level"    : "INFO",
                        "formatter": "standard",
                        "class"    : "logging.StreamHandler",
                        "stream"   : "ext://sys.stdout",
                },
                "file"  : {
                        "class"      : "logging.handlers.RotatingFileHandler",
                        "level"      : "INFO",
                        "formatter"  : "detailed",
                        "filename"   : "arcbest_api.log",
                        "maxBytes"   : 1024 * 1024 * 5,  # 5 MB
                        "backupCount": 4,
                }
        },

        "loggers"                 : {
                "root": {"handlers": ["default"], "level": "INFO", "propagate": False
                         }
        }
}

# logging.config.dictConfig(logging_config)

pp = pprint.PrettyPrinter(indent=4)


def bool_to_str(x: bool | None) -> str:
    return 'Y' if x else 'N'


def get_current_date_as_tuple() -> tuple:
    now = datetime.now()
    return (now.day, now.month, now.year)
