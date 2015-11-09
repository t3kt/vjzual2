try:
	import vjz_util as util
except ImportError:
	import vjz.util as util

setattrs = util.setattrs
setexpr = util.setexpr

class Smoother:
	def __init__(self, comp):
		self.comp = comp

	def Initialize(self):
		page = self.comp.appendCustomPage('Smoother')
		setattrs(page.appendToggle('Active', label='Active'),
		         default=False)
		modes = self.comp.op('modes')
		setattrs(page.appendMenu('Mode', label='Smoother Mode'),
		         menuNames=modes.col('name')[1:],
		         menuLabels=modes.col('label')[1:],
		         default='gauss')
		setattrs(page.appendFloat('Filterwidth', label='Filter Width'),
		         normMin=0,
		         normMax=2,
		         default=1)
		setattrs(page.appendFloat('Filtereffect', label='Filter Effect'),
		         normMin=0,
		         normMax=2,
		         default=1)
		setattrs(page.appendFloat('Lag', label='Lag Amount'),
		         normMin=0,
		         normMax=1.5,
		         default=0.3)
		setattrs(page.appendFloat('Overshoot', label='Overshoot'),
		         normMin=0,
		         normMax=1,
		         default=0)

		for init in self.comp.ops('*/init'):
			init.run()
