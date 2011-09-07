DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'panda_experiments',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file_logging': {
            'level' : 'DEBUG',
            'class' : 'logging.handlers.RotatingFileHandler',
            'backupCount' : 5,
            'maxBytes': 5000000,
            'filename': 'django.log'
            },
        'db_logging': {
            'level' : 'DEBUG',
            'class' : 'logging.handlers.RotatingFileHandler',
            'backupCount' : 5,
            'maxBytes': 5000000,
            'filename': 'django-db.log'
            },
        },
        
    'loggers': {
        'django' : {
            'handlers': ['file_logging'],
            'level' : 'DEBUG',
            'propagate' : False,
            },
        'django.db' : {
            'handlers' : ['db_logging'],
            'level' : 'DEBUG',
            'propagate': False,
            },
        }
    }
