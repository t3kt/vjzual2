try:
	from vjz_module import VjzModule
except ImportError:
	from vjz.module import VjzModule

try:
	import vjz_util as util
except ImportError:
	import vjz.util as util

setattrs = util.setattrs

class ConstantModule(VjzModule):
	def __init__(self, comp):
		VjzModule.__init__(self, comp)

	def Initialize(self):
		VjzModule.Initialize(self)
		m = self._comp
		page = self.GetModParamsPage()

		setattrs(page.appendRGBA('Mparcolor', label='Color'),
		         default=1)

		for init in m.ops('*/init'):
			init.run()
