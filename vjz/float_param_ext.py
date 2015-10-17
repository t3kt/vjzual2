from vjz_params import VjzParam
import vjz_util as util

class FloatParam(VjzParam):
	def __init__(self, comp):
		VjzParam.__init__(self, comp)

	def Initialize(self):
		VjzParam.Initialize(self)
		slider = self._comp.op('slider')
		self.ApplyBaseProxyExprs(slider)
		util.setexpr(self._comp.par.Partype, '"float"')
		util.setParExprs(slider,
		                 w='op("rootpanel").par.w - (0 if parent().par.Parhidelabel else op("label").par.w)',
		                 h='op("rootpanel").par.h')

	def GetValue(self):
		return self._comp.op('slider').GetValue()

	def SetValue(self, value):
		return self._comp.op('slider').PushValue(value)
