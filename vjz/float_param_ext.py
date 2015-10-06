from vjz_params import VjzParam
import vjz_util as util

setattrs = util.setattrs
overrideRows = util.overrideRows

class FloatParam(VjzParam):
	def __init__(self, comp):
		VjzParam.__init__(self, comp)

	def Initialize(self):
		VjzParam.Initialize(self)
		page = self.GetParamPage()
		setattrs(page.appendMenu('Parsliderstyle', label='Slider Style')[0],
		         menuNames=['std', 'xfade'],
		         menuLabels=['Standard', 'X-Fade'])
		slider = self._comp.op('slider')
		self.ApplyBaseProxyExprs(slider)
		util.ApplyPythonProxyExprs(slider, 'ext.vjzpar.par.',
		                          Pctlsliderstyle='Parsliderstyle')
