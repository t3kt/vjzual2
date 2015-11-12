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
		util.ApplyPythonProxyExprs(menu, 'parent().par.',
		                           Pctllistsize='Parlistsize')
		util.setattrs(page.appendInt('Parnumoptions', label='Number of Options')[0],
		              min=1,
		              clampMin=True,
		              default=1)
		util.setexpr(self._comp.par.Partype, '"menu"')
		util.setParExprs(menu,
		                 w='op("rootpanel").par.w - (0 if parent().par.Parhidelabel else op("label").par.w)',
		                 h='op("rootpanel").par.h')
		par = self.TargetPar
		if par is not None:
			self._comp.par.Parnumoptions = len(par.menuNames)

	@property
	def TargetPar(self):
		return self._comp.op('menu').TargetPar

	def GetValue(self):
		return self._comp.op('menu').GetValue()

	def SetValue(self, value):
		return self._comp.op('menu').PushValue(value)
