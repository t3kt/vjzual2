try:
	from vjz_module import VjzModule
except ImportError:
	from vjz.module import VjzModule

import vjz_util as util
setattrs = util.setattrs

class ColorAdjModule(VjzModule):
	def __init__(self, comp):
		VjzModule.__init__(self, comp)


	def Initialize(self):
		VjzModule.Initialize(self)
		page = self.GetModParamsPage()
		setattrs(page.appendFloat('Mparsaturation', label='Saturation')[0],
			default=0.5)
		setattrs(page.appendFloat('Mparhue', label='Hue')[0],
			default=0.5)
		setattrs(page.appendFloat('Mparbrightness', label='Brightness')[0],
			default=0.5)
		setattrs(page.appendFloat('Mparcontrast', label='Contrast')[0],
			default=0.5)
		for init in self._comp.ops('shell/init', 'overlay/init', '*_param/init'):
			init.run()

