class plugin:
	def __init__(self):
		pass

	def event_handler(self, event_name, *args, **kwargs):
		if hasattr(self, event_name):
			enabled = True
			func = getattr(self, event_name, None)
			if hasattr(self, '__enabled__'):
				enabled = getattr(self, '__enabled__', None)
			if callable(func) and enabled:
				return func(*args, **kwargs)