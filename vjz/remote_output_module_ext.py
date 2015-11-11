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

class RemoteOutputModule(VjzModule):
	def __init__(self, comp):
		VjzModule.__init__(self, comp)

	def Initialize(self):
		VjzModule.Initialize(self)
		m = self._comp
		page = self.GetModParamsPage()

		setattrs(page.appendMenu('Mparoutmode', label='Output Mode'),
		         menuNames=['touch', 'spout'],
		         menuLabels=['Touch Out', 'Spout'],
		         default='')

		setattrs(page.appendInt('Mparport', label='Network Port'),
		         normMin=0, min=0, clampMin=True,
		         normMax=20000, max=20000, clampMax=False,
		         default=9000)
		setattrs(page.appendInt('Mparfps', label='FPS'),
		         normMin=1, min=1, clampMin=True,
		         normMax=100, max=100, clampMax=True,
		         default=30)
		setattrs(page.appendStr('Mparspoutname', label='Spout Name'),
		         default='vjz2out')
		setattrs(page.appendMenu('Mparcodec', label='Video Codec'),
		         menuNames=['uncompressed', 'hapq'],
		         menuLabels=['Uncompressed', 'HAP Q'],
		         default='hapq')

		m.par.Modhasadvanced = False

		for init in m.ops('*/init'):
			init.run()
