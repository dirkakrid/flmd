import plugin

class test(plugin.plugin):
	def __init__(self):
		pass

	def onload(self, data):
		data['filename'] = 'content/hello.md'
		return data