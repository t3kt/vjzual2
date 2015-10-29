try:
	from vjz_module import VjzModule
except ImportError:
	from vjz.module import VjzModule

import vjz_util as util
setattrs = util.setattrs

class TintModule(VjzModule):
	def __init__(self, comp):
		VjzModule.__init__(self, comp)


	def Initialize(self):
		VjzModule.Initialize(self)
		page = self.GetModParamsPage()
		setattrs(page.appendFloat('Mparlevel', label='Level')[0],
			default=0.5)
		setattrs(page.appendFloat('Mparsaturation', label='Saturation')[0],
			default=0.5)
		setattrs(page.appendFloat('Mparhue', label='Hue')[0],
			default=0.5)
		setattrs(page.appendFloat('Mparbrightness', label='Brightness')[0],
			default=0.5)
		page.appendToggle('Mparinvert', label='Invert')
		modes = op('/_/components/mono_mode_menu_options')
		setattrs(page.appendMenu('Mparmonorgb', label='Mono Mode'),
		         menuNames=modes.col('name')[1:],
		         menuLabels=modes.col('label')[1:],
		         default='luminance')
		for init in self._comp.ops('shell/init', 'overlay/init', '*_param/init'):
			init.run()

