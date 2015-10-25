try:
	from vjz_module import VjzModule
except ImportError:
	from vjz.module import VjzModule

import vjz_util as util
setattrs = util.setattrs
setexpr = util.setexpr

class NoiseGenModule(VjzModule):
	def __init__(self, comp):
		VjzModule.__init__(self, comp)

	def Initialize(self):
		VjzModule.Initialize(self)
		m = self._comp
		page = m.GetModParamsPage()
		setattrs(page.appendFloat('Mparperiod', label='Period')[0],
		         min=0, clampMin=True, normMax=4, default=1)
		setattrs(page.appendFloat('Mpargain', label='Harmonic Gain')[0],
		         min=0, clampMin=True, normMax=2, default=1)
		page.appendXYZ('Mparrate', label='Rate')
		setattrs(page.appendMenu('Mparalphamode', label='Alpha Mode')[0],
		         menuNames=['zero', 'one', 'random'],
		         menuLabels=['Zero', 'One', 'Noise'])
		setattrs(page.appendToggle('Mparmono', label='Monochrome')[0],
		         default=True)

		for init in m.ops('*/init'):
			init.run()
