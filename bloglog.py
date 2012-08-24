LOGGING = {
	'version': 1,
	'disable_existing_loggers': True,
	'formatters': {
		'default': {
			'format': '%(levelname)s %(asctime)s %(module)s %(name)s %(process)d %(thread)d %(message)s'
		}
	},
	'filters': {

	},
	'handlers': {
		'file_handler': {
			'class': 'logging.handlers.TimedRotatingFileHandler',
			'level': 'DEBUG',
			'formatter': 'default',
			'when': 'midnight',
			'filename': '/data/logs/articles.log'
		},
		'root_handler': {
			'class': 'logging.handlers.TimedRotatingFileHandler',
			'level': 'DEBUG',
			'formatter': 'default',
			'when': 'midnight',
			'filename': '/data/logs/blog.log'
		}
	},
	'loggers': {
		'articles': {
			'level': 'DEBUG',
			'handlers': ['file_handler'],
			'propagate': False 
		},
		'django': {
			'level': 'DEBUG',
			'handlers': ['file_handler'],
			'propagate': False
		}
	},
	'root': {
		'level': 'DEBUG',
		'hanlders': ['file_handler']	
	}
}
