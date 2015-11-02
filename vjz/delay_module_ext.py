try:
	from vjz_module import VjzModule
except ImportError:
	from vjz.module import VjzModule

try:
	import vjz_util as util
except ImportError:
	import vjz.util as util

setattrs = util.setattrs
setexpr = util.setexpr

class DelayModule(VjzModule):
	def __init__(self, comp):
		VjzModule.__init__(self, comp)

	def Initialize(self):
		VjzModule.Initialize(self)
		m = self._comp
		page = self.GetModParamsPage()

		page.appendFloat('Mparlevel', label='Level')
		page.appendFloat('Mparlength', label='Length')
		setattrs(page.appendInt('Mparcachesize', label='Cache Size')[0],
		         normMin=1,
		         normMax=128,
		         min=1,
		         clampMin=True,
		         default=32)

		for init in m.ops('*/init'):
			init.run()
