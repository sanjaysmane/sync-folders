#!/usr/bin/env python
import logging.config
import datetime

def loggerFunc(fname):
    logging_config = { 
        'version': 1,
        'formatters': { 
            'standard': { 
                'format': '%(asctime)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': { 
            'stream': { 
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
            'file': { 
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.FileHandler',
                'filename': fname
            },
        },
        'loggers': { 
            __name__: { 
                'handlers': ['stream', 'file'],
                'level': 'INFO',
                'propagate': False
            },
        } 
    }
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)
    return logger

if __name__ == '__main__':
    main()