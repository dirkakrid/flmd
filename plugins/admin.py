import plugin

class admin(plugin.plugin):
	__enabled__ 	= True
	__priority__ 	= 9

	def init(self, *args, **kwargs):
		if args[0].startswith('admin'):
			print 'admin'