import plugin

class test(plugin.plugin):
	def __init__(self):
		pass

	def onload(self, name='', *args, **kwargs):
		print '\n\nonload, {}\n\n'.format(name)