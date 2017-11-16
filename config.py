# App Config

class BaseConfig(object):
	DEBUG = False
	SECRET_KEY = 'hard to guess string'

class DevelopmentConfig(BaseConfig):
	DEBUG = True

class ProductionConfig(BaseConfig):
	DEBUG = False
	SECRET_KEY = "not stupid enough to commit to GitHub"