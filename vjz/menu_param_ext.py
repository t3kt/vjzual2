from vjz_params import VjzParam
import vjz_util as util

class MenuParam(VjzParam):
	def __init__(self, comp):
		VjzParam.__init__(self, comp)

	def Initialize(self):
		VjzParam.Initialize(self)
		comp = self._comp
		page = self.GetParamPage()
		util.setattrs(page.appendInt('Parlistsize', label='List Items')[0],
					  min=1,
					  normMin=1,
					  clampMin=1,
					  normMax=10,
					  default=5)
		util.setattrs(page.appendInt('Parnumoptions', label='Number of Options')[0],
		              min=1,
		              clampMin=True,
		              default=1)
		menu = comp.op('menu')
		self.ApplyBaseProxyExprs(menu)
		util.ApplyPythonProxyExprs(menu, 'ext.vjzpar.par.',
		                          Pctllistsize='Parlistsize')
		util.setexpr(comp.par.Partype, '"menu"')
		util.setParExprs(menu,
		                 w='op("rootpanel").par.w - (0 if parent().par.Parhidelabel else op("label").par.w)',
		                 h='op("rootpanel").par.h')
		par = self.TargetPar
		if par is not None:
			util.setParExprs(comp,
			                 Parnumoptions='len(me.TargetPar.menuNames)')

	@property
	def TargetPar(self):
		return self._comp.op('menu').TargetPar

	def GetValue(self):
		return self._comp.op('menu').GetValue()

	def SetValue(self, value):
		return self._comp.op('menu').PushValue(value)
