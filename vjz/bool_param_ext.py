from vjz_params import VjzParam
import vjz_util as util

class BoolParam(VjzParam):
	def __init__(self, comp):
		VjzParam.__init__(self, comp)

	def Initialize(self):
		VjzParam.Initialize(self)
		page = self.GetParamPage()
		page.appendStr('Parontext', label='Button On Text')
		page.appendStr('Parofftext', label='Button Off Text')
		page.appendStr('Paroffhelptext', label='Button Off Help Text')
		toggle = self._comp.op('toggle')
		self.ApplyBaseProxyExprs(toggle)
		util.ApplyPythonProxyExprs(toggle, 'parent().par.',
		                           Pctlontext='Parontext',
		                           Pctlofftext='Parofftext',
		                           Pctloffhelptext='Paroffhelptext')
		util.setexpr(self._comp.par.Partype, '"bool"')
		util.setParExprs(toggle,
		                 w='op("rootpanel").par.w - (0 if parent().par.Parhidelabel else op("label").par.w)',
		                 h='op("rootpanel").par.h')
		mapping = self._comp.op('midi_mapping')
		if mapping is not None:
			self.ApplyMappingProxyExprs(mapping)

	@property
	def TargetPar(self):
		return self._comp.op('toggle').TargetPar

	def GetValue(self):
		return self._comp.op('toggle').GetValue()

	def SetValue(self, value):
		return self._comp.op('toggle').PushValue(value)
