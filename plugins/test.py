import plugin

class test(plugin.plugin):
	def __init__(self):
		pass

	def onload(self, data):
		data[0] = 'content/hello.md'