class plugin:
	def __init__(self):
		pass

	def event_handler(self, event_name, *args, **kwargs):
		func = self.get_function(event_name)
		enabled = self.get_variable('__enabled__', False)
		if enabled:
			try:
				return func(*args, **kwargs)
			except TypeError:
				return args, kwargs

	def get_variable(self, name, default=None):
		if hasattr(self, name):
			return getattr(self, name)
		return default

	def get_function(self, name, default=None):
		if hasattr(self, name):
			func = getattr(self, name, None)
			if callable(func):
				return func
		return default