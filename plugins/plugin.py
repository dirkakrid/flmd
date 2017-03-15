class plugin:
	def __init__(self):
		pass

	def handle_event(self, event_name, *args, **kwargs):
		if hasattr(self, event_name):
			func = getattr(self, event_name, None)
			if callable(func):
				return func(*args, **kwargs)