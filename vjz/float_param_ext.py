from vjz_params import VjzParam
import vjz_util as util

class FloatParam(VjzParam):
	def __init__(self, comp):
		VjzParam.__init__(self, comp)

	def Initialize(self):
		VjzParam.Initialize(self)
		comp = self._comp
		page = self.GetParamPage()
		page.appendFloat('Parnormrange', label='Normalized Range', size=2)
		page.appendFloat('Parrange', label='Range', size=2)
		page.appendToggle('Parclampmin', label='Clamp Min')
		page.appendToggle('Parclampmax', label='Clamp Max')
		par = self.TargetPar
		if par is not None:
			util.setParExprs(comp,
			                 Parnormrange1='me.TargetPar.normMin',
			                 Parnormrange2='me.TargetPar.normMax',
			                 Parrange1='me.TargetPar.min',
			                 Parrange2='me.TargetPar.max',
			                 Parclampmin='me.TargetPar.clampMin',
			                 Parclampmax='me.TargetPar.clampMax')
		else:
			print('target par not available on init for ', comp.path)

		slider = comp.op('slider')
		self.ApplyBaseProxyExprs(slider)
		util.setexpr(comp.par.Partype, '"float"')
		util.setParExprs(slider,
		                 w='op("rootpanel").par.w - (0 if parent().par.Parhidelabel else op("label").par.w)',
		                 h='op("rootpanel").par.h')

	@property
	def TargetPar(self):
		return self._comp.op('slider').TargetPar

	def GetValue(self):
		return self._comp.op('slider').GetValue()

	def SetValue(self, value):
		return self._comp.op('slider').PushValue(value)
