class plugin:
	def __init__(self):
		pass

	def handle_event(self, event_name):
		if hasattr(self, event_name):
			func = getattr(self, event_name, None)
			if callable(func):
				func()