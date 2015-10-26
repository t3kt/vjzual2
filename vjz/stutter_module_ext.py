try:
	from vjz_module import VjzModule
except ImportError:
	from vjz.module import VjzModule

import vjz_util as util
setattrs = util.setattrs

class StutterModule(VjzModule):
	def __init__(self, comp):
		VjzModule.__init__(self, comp)


	def Initialize(self):
		VjzModule.Initialize(self)
		page = self.GetModParamsPage()
		
		page.appendFloat('Mparlevel', label='Level')
		
		setattrs(page.appendInt('Mparcachesize', label='Cache Size')[0],
			normMin=1,
			normMax=128,
			min=1,
			clampMin=True,
			default=32)

		setattrs(page.appendFloat('Mparlength', label='Playback Length')[0],
			default=1)
		setattrs(page.appendFloat('Mparplayrate', label='Playback Rate')[0],
		         normMin=-1,
		         normMax=5,
		         default=1)

		page.appendToggle('Mparplayback', label='Playback')
		setattrs(page.appendToggle('Mparrecord', label='Record')[0],
		         default=True)
		
		for init in self._comp.ops('shell/init', 'overlay/init', '*_param/init'):
			init.run()

