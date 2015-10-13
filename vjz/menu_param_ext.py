from vjz_params import VjzParam
import vjz_util as util

class MenuParam(VjzParam):
	def __init__(self, comp):
		VjzParam.__init__(self, comp)

	def Initialize(self):
		VjzParam.Initialize(self)
		page = self.GetParamPage()
		util.setattrs(page.appendInt('Parlistsize', label='List Items')[0],
					  min=1,
					  normMin=1,
					  clampMin=1,
					  normMax=10,
					  default=5)
		menu = self._comp.op('menu')
		self.ApplyBaseProxyExprs(menu)
		util.ApplyPythonProxyExprs(menu, 'ext.vjzpar.par.',
		                          Pctllistsize='Parlistsize')

	def GetValue(self):
		return self._comp.op('menu').GetValue()

	def SetValue(self, value):
		return self._comp.op('menu').PushValue(value)
