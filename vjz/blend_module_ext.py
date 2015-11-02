try:
	from vjz_module import VjzModule
except ImportError:
	from vjz.module import VjzModule

try:
	import vjz_util as util
except ImportError:
	import vjz.util as util

setattrs = util.setattrs

class BlendModule(VjzModule):
	def __init__(self, comp):
		VjzModule.__init__(self, comp)

	def Initialize(self):
		VjzModule.Initialize(self)
		m = self._comp
		page = self.GetModParamsPage()

		page.appendToggle('Mparmodinput', label='Use Module Input')
		setattrs(page.appendFloat('Mparcross', label='Cross Fade')[0],
		         normMin=-1, min=-1, clampMin=True,
		         normMax=1, max=1, clampMax=True,
		         default=0)
		page.appendToggle('Mparswap', label='Swap Order')
		compopts = op(var('compositemenuopts'))
		setattrs(page.appendMenu('Mparoperand', label='Composite Operator')[0],
		         menuNames=compopts.col('name')[1:],
		         menuLabels=compopts.col('label')[1:])
		page.appendToggle('Mparshowinput', label='Show Input')

		for init in m.ops('*/init'):
			init.run()
