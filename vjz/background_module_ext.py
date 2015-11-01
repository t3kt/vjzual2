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

class BackgroundModule(VjzModule):
	def __init__(self, comp):
		VjzModule.__init__(self, comp)

	def Initialize(self):
		VjzModule.Initialize(self)
		m = self._comp
		page = self.GetModParamsPage()

		page.appendFloat('Mparlevel', label='Level')
		setattrs(page.appendMenu('Mparbgmode', label='Background Mode')[0],
		         menuNames=['constant', 'source'],
		         menuLabels=['Constant', 'Source Video'],
		         default='constant')
		page.appendRGBA('Mparbgcolor', label='Background Color')
		m.par.Mparbgcolorr.default = 0
		m.par.Mparbgcolorg.default = 0
		m.par.Mparbgcolorb.default = 0
		m.par.Mparbgcolora.default = 1

		for init in m.ops('*/init'):
			init.run()
