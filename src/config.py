import logging
import logging.config


#AI_MODEL = "gpt-5-nano"
AI_MODEL = "gpt-5-mini"

ASPECT_LABEL = {
    "AI": "Avaliação Inicial",
    "AP": "Apresentação",
    "CR": "Coerência",
    "CS": "Coesão",
    "LG": "Linguagem",
    "TM": "Tema",
    "TT": "Tipo Textual",
}


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        __name__: {
            "handlers": ["console"],    
            "level": "DEBUG",
            "propagate": False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)
