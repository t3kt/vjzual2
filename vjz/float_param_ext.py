if False:
	from vjz.params import VjzParam
else:
	from vjz_params import VjzParam
if False:
	import vjz.util as util
else:
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
		slider = comp.op('slider')
		self.ApplyBaseProxyExprs(slider)
		util.ApplyPythonProxyExprs(slider, 'ext.vjzpar.par.',
		                           Pctlnormrange1='Parnormrange1',
		                           Pctlnormrange2='Parnormrange2',
		                           Pctlrange1='Parrange1',
		                           Pctlrange2='Parrange2',
		                           Pctlclampmin='Parclampmin',
		                           Pctlclampmax='Parclampmax')
		util.setexpr(comp.par.Partype, '"float"')
		util.setParExprs(slider,
		                 w='op("rootpanel").par.w - (0 if parent().par.Parhidelabel else op("label").par.w)',
		                 h='op("rootpanel").par.h')
		self.ApplyMappingProxyExprs(comp.op('midi_mapping'))

	@property
	def TargetPar(self):
		return self._comp.op('slider').TargetPar

	def GetValue(self):
		return self._comp.op('slider').GetValue()

	def SetValue(self, value):
		return self._comp.op('slider').PushValue(value)
