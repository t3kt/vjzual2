try:
	from vjz_module import VjzModule
except ImportError:
	from vjz.module import VjzModule

try:
	import vjz_util as util
except ImportError:
	import vjz.util as util

setattrs = util.setattrs
setParExprs = util.setParExprs

class WarpModule(VjzModule):
	def __init__(self, comp):
		VjzModule.__init__(self, comp)

	def Initialize(self):
		VjzModule.Initialize(self)
		m = self._comp
		page = self.GetModParamsPage()
		setattrs(page.appendFloat('Mparlevel', label='Level'),
		         default=1)
		displacePars = m.op('displace').par
		setattrs(page.appendMenu('Mparhorzsource', label='Horizontal Source'),
		         menuNames=displacePars.horzsource.menuNames,
		         menuLabels=displacePars.horzsource.menuLabels,
		         default='red')
		setattrs(page.appendMenu('Mparvertsource', label='Vertical Source'),
		         menuNames=displacePars.vertsource.menuNames,
		         menuLabels=displacePars.vertsource.menuLabels,
		         default='blue')
		setattrs(page.appendXY('Mpardisplaceweight', label='Displace Weight'),
		         normMin=-2, normMax=2, default=0)
		setattrs(page.appendFloat('Mpardisplaceweightscale', label='Displace Weight Scale'),
		         normMin=0, normMax=2, default=0)
		setattrs(page.appendFloat('Mparuvweight', label='UV Weight'),
		         normMin=-5, normMax=5, default=1)
		setattrs(page.appendMenu('Mparextend', label='Extend'),
		         menuNames=displacePars.extend.menuNames,
		         menuLabels=displacePars.extend.menuLabels,
		         default='mirror')

		setParExprs(m,
		            Modfullheight='280 if me.par.Modshowviewers else 180',
		            Modcompactheight='240 if me.par.Modshowviewers else 140')
		m.par.Modhasadvanced = True
		m.par.Modhasviewers = True

		for init in m.ops('*/init'):
			init.run()
