import plugin

class admin(plugin.plugin):
	__enabled__ 	= True
	__priority__ 	= 0

	def init(self, *args, **kwargs):
		if kwargs.get('url', '').startswith('admin'):
			print 'admin'