try:
	from vjz_module import VjzModule
except ImportError:
	from vjz.module import VjzModule

import vjz_util as util
setattrs = util.setattrs
setexpr = util.setexpr

class TransformModule(VjzModule):
	def __init__(self, comp):
		VjzModule.__init__(self, comp)

	def Initialize(self):
		VjzModule.Initialize(self)
		m = self._comp
		page = m.GetModParamsPage()

		page.appendFloat('Mparlevel', label='Level')

		transform = m.op('transform')

		setattrs(page.appendMenu('Mparextend', label='Extend')[0],
			menuNames=transform.par.extend.menuNames,
			menuLabels=transform.par.extend.menuLabels,
			default='mirror')

		setattrs(page.appendXY('Mpars', label='Scale'),
			normMin=-1,
			normMax=3,
			default=1)
		setattrs(page.appendFloat('Mparscale', label='Uniform Scale')[0],
			normMin=-1,
			normMax=3,
			default=1)
		setattrs(page.appendXY('Mpart', label='Translate'),
			normMin=-1,
			normMax=1,
			default=0)
		setattrs(page.appendFloat('Mparrotate', label='Rotate')[0],
			normMin=-360,
			normMax=360,
			default=0)

		setattrs(page.appendMenu('Mparorder', label='Transform Order')[0],
			menuNames=transform.par.xord.menuNames,
			menuLabels=transform.par.xord.menuLabels,
			default=transform.par.xord.default)

		setattrs(m.par,
		         Modfullheight=192,
		         Modcompactheight=152,
		         Modhasadvanced=True,
		         Modhasviewers=False)

		for init in m.ops('shell/init', 'overlay/init', '*_param/init'):
			init.run()
