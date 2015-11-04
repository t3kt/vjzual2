try:
	from vjz_module import VjzModule
except ImportError:
	from vjz.module import VjzModule

try:
	import vjz_util as util
except ImportError:
	import vjz.util as util

setattrs = util.setattrs

class IterateModule(VjzModule):
	def __init__(self, comp):
		VjzModule.__init__(self, comp)

	def Initialize(self):
		VjzModule.Initialize(self)
		m = self._comp
		page = self.GetModParamsPage()
		setattrs(page.appendFloat('Mparlevel', label='Level'),
		         default=1)
		setattrs(page.appendInt('Mparcount', label='Count'),
		         normMin=1, min=1, clampMin=True,
		         normMax=32,
		         default=4)
		setattrs(page.appendFloat('Mparalpha', label='Alpha'),
		         normMin=0, normMax=1, default=1)
		setattrs(page.appendFloat('Mparstartscale', label='Start Uniform Scale'),
		         normMin=0, normMax=10, default=1)
		setattrs(page.appendXYZ('Mparstarts', label='Start Scale'),
		         normMin=-1, normMax=3, default=1)
		setattrs(page.appendXYZ('Mparstartt', label='Start Translate'),
		         normMin=-4, normMax=4, default=0)
		setattrs(page.appendXYZ('Mparstartr', label='Start Rotate'),
		         normMin=-180, normMax=180, default=0)
		setattrs(page.appendFloat('Mparstartalpha', label='Start Alpha'),
		         normMin=0, normMax=1, default=1)

		setattrs(page.appendFloat('Mparendscale', label='End Uniform Scale'),
		         normMin=0, normMax=10, default=1)
		setattrs(page.appendXYZ('Mparends', label='End Scale'),
		         normMin=-1, normMax=3, default=1)
		setattrs(page.appendXYZ('Mparendt', label='End Translate'),
		         normMin=-4, normMax=4, default=0)
		setattrs(page.appendXYZ('Mparendr', label='End Rotate'),
		         normMin=-180, normMax=180, default=0)
		setattrs(page.appendFloat('Mparendalpha', label='End Alpha'),
		         normMin=0, normMax=1, default=1)

		m.par.Modfullheight = 310
		m.par.Modcompactheight = 210
		m.par.Modhasadvanced = True

		for init in m.ops('*/init'):
			init.run()
