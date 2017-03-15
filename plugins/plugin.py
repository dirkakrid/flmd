class plugin:
	def __init__(self):
		pass

	def handle_event(self, event_name, data):
		if hasattr(self, event_name):
			func = getattr(self, event_name, None)
			enabled = True
			if hasattr(self, '__enabled__'):
				enabled = getattr(self, '__enabled__', None)
			if callable(func) and enabled:
				return func(data)