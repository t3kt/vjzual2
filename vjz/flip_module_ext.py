try:
	from vjz_module import VjzModule
except ImportError:
	from vjz.module import VjzModule

try:
	import vjz_util as util
except ImportError:
	import vjz.util as util

setattrs = util.setattrs

class FlipModule(VjzModule):
	def __init__(self, comp):
		VjzModule.__init__(self, comp)

	def Initialize(self):
		VjzModule.Initialize(self)
		m = self._comp
		page = self.GetModParamsPage()

		page.appendFloat('Mparlevel', label='Level')
		page.appendToggle('Mparflipx', label='Flip X')
		page.appendToggle('Mparflipy', label='Flip Y')

		compopts = op(var('compositemenuopts'))
		setattrs(page.appendMenu('Mparoperand', label='Composite Operator')[0],
		         menuNames=compopts.col('name')[1:],
		         menuLabels=compopts.col('label')[1:])

		for init in m.ops('*/init'):
			init.run()
