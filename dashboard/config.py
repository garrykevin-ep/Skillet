class conf(object):
	"""docstring for context"""
	content = 'Tests'

	def context(self):
		# context = {'content' : self.content}
		return {'content' : self.content}
		