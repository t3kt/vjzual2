try:
	from vjz_module import VjzModule
except ImportError:
	from vjz.module import VjzModule

import vjz_util as util
setattrs = util.setattrs
setexpr = util.setexpr

class GridGenModule(VjzModule):
	def __init__(self, comp):
		VjzModule.__init__(self, comp)

	def Initialize(self):
		VjzModule.Initialize(self)
		m = self._comp
		page = self.GetModParamsPage()
		setattrs(page.appendInt('Mparrows', label='Rows')[0],
		         normMin=2, min=2, clampMin=True,
		         normMax=30, max=30)
		setattrs(page.appendInt('Mparcols', label='Columns')[0],
		         normMin=2, min=2, clampMin=True,
		         normMax=30, max=30)
		page.appendRGBA('Mparptcolor', label='Point Color')
		m.par.Mparptcolorr.default = 1
		m.par.Mparptcolorg.default = 1
		m.par.Mparptcolorb.default = 1
		m.par.Mparptcolora.default = 1
		page.appendRGBA('Mparlncolor', label='Line Color')
		m.par.Mparlncolorr.default = 1
		m.par.Mparlncolorg.default = 1
		m.par.Mparlncolorb.default = 1
		m.par.Mparlncolora.default = 1
		page.appendRGBA('Mparbgcolor', label='Background Color')
		m.par.Mparbgcolorr.default = 0
		m.par.Mparbgcolorg.default = 0
		m.par.Mparbgcolorb.default = 0
		m.par.Mparbgcolora.default = 1
		setattrs(page.appendXY('Mparrate', label='Rate'),
		         normMin=-5, normMax=5, default=0)
		setattrs(page.appendFloat('Mparptscale', label='Point Scale')[0],
		         normMin=5, normMax=100, default=10)
		setattrs(page.appendFloat('Mparlnwidth', label='Line Width')[0],
		         normMin=0, normMax=10, default=1)

		for init in m.ops('*/init'):
			init.run()
