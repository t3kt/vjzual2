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

class KaleidoModule(VjzModule):
	def __init__(self, comp):
		VjzModule.__init__(self, comp)

	def Initialize(self):
		VjzModule.Initialize(self)
		m = self._comp
		page = m.GetModParamsPage()

		page.appendFloat('Mparlevel', label='Level')
		setattrs(page.appendFloat('Mparpreoffset', label='Pre Offset'),
		         normMin=-4,
		         normMax=4,
		         default=0)
		setattrs(page.appendFloat('Mparpostoffset', label='Post Offset'),
		         normMin=-4,
		         normMax=4,
		         default=0)
		setattrs(page.appendXY('Mpart', label='Translate'),
		         normMin=-0.6,
		         normMax=0.6,
		         default=0)
		setattrs(page.appendFloat('Mparsegments', label='Segments'),
		         normMin=-2,
		         normMax=8,
		         default=2)
		extendModes = op('/_/components/top_transform_extend_menu_options')
		setattrs(page.appendMenu('Mparextend', label='Extend Mode'),
		         menuNames=extendModes.col('name')[1:],
		         menuLabels=extendModes.col('label')[1:],
		         default='mirror')

		for init in m.ops('*/init'):
			init.run()

class KaleidoCore:
	def __init__(self, core):
		self.core = core

	def Initialize(self):
		page = self.core.appendCustomPage('Kaleido')
		setattrs(page.appendFloat('Preoffset', label='Pre Offset'),
		         normMin=-4,
		         normMax=4,
		         default=0)
		setattrs(page.appendFloat('Postoffset', label='Post Offset'),
		         normMin=-4,
		         normMax=4,
		         default=0)
		setattrs(page.appendXY('Translate', label='Translate'),
		         normMin=-0.6,
		         normMax=0.6,
		         default=0)
		setattrs(page.appendFloat('Segments', label='Segments'),
		         normMin=-2,
		         normMax=8,
		         default=2)
		extendModes = op('/_/components/top_transform_extend_menu_options')
		setattrs(page.appendMenu('Inputextenduv', label='Input Extend Mode UV'),
		         menuNames=extendModes.col('name')[1:],
		         menuLabels=extendModes.col('label')[1:],
		         default='mirror')
		page.appendDAT('Pixelshader', label='Pixel Shader')
