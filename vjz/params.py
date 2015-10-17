__author__ = 'tekt'

print('params.py initializing')

if False:
	import vjz.util as util
else:
	import vjz_util as util

class ParControl:
	def __init__(self, comp):
		self._comp = comp

	def GetParControlPage(self):
		return self._comp.appendCustomPage('ParCtrl')

	def Initialize(self):
		page = self.GetParControlPage()
		page.appendOP('Pctlop', label='Target Operator')
		page.appendStr('Pctlpar', label='Target Parameter')
		page.appendStr('Pctllabel', label='UI Label')
		page.appendStr('Pctlchan', label='Output Channel')
		page.appendStr('Pctlhelptext', label='Control Help Text')
		util.setattrs(page.appendInt('Pctlfontsize', label='Font Size')[0],
					  default=12, min=1, normMin=1, normMax=30, clampMin=True)

	@property
	def TargetOp(self):
		return self._comp.par.Pctlop.eval()

	@property
	def TargetPar(self):
		target = self.TargetOp
		pname = self._comp.par.Pctlpar.eval()
		if target and hasattr(target.par, pname):
			return getattr(target.par, pname)

	def _PullIntoPanelValue(self, name):
		p = self.TargetPar
		if p is not None:
			setattr(self._comp.panel, name, p.eval())

	def PushValue(self, value):
		p = self.TargetPar
		if p is not None:
			p.val = value

	def GetValue(self):
		p = self.TargetPar
		if p is not None:
			return p.eval()

	def ResetToDefault(self):
		p = self.TargetPar
		if p is not None:
			p.val = p.default

class VjzParam:
	def __init__(self, comp):
		self._comp = comp
		comp.tags.add('vjzpar')

	def GetParamPage(self):
		return self._comp.appendCustomPage('VjzParam')

	def Initialize(self):
		self._comp.par.inshortcut = 'vjzpar'
		page = self.GetParamPage()
		page.appendOP('Parop', label='Target Operator')
		page.appendStr('Parpar', label='Target Parameter')
		page.appendStr('Parlocalname', label='Local Name')
		page.appendStr('Parid', label='Parameter Unique ID')
		page.appendStr('Partype', label='Parameter Type')
		page.appendStr('Parlabel', label='UI Label')
		page.appendStr('Parchan', label='Output Channel')
		page.appendStr('Parhelptext', label='Help Text')
		page.appendToggle('Parhidelabel', label='Hide Label')
		util.setattrs(page.appendInt('Parfontsize', label='Font Size')[0],
					  default=12, min=1, normMin=1, normMax=30, clampMin=True)
		util.setattrs(page.appendMenu('Paruimode', label='UI Mode')[0],
		              menuNames=['ctrl', 'midiedit'],
		              menuLabels=['Controls', 'Edit MIDI'])
		if hasattr(self._comp.ext, 'vjzmod'):
			util.setexpr(self._comp.par.Parid, 'ext.vjzmod.par.Modname + ":" + me.par.Parlocalname')
		label = self._comp.op('label')
		label.par.top = './bg'
		util.setParExprs(label,
		                 w='op("rootpanel").par.w / 3',
		                 h='op("rootpanel").par.h',
		                 display='not parent().par.Parhidelabel')

	def ApplyBaseProxyExprs(self, ctrlComp):
		util.ApplyPythonProxyExprs(ctrlComp, 'ext.vjzpar.par.',
		                     Pctlop='Parop',
		                     Pctlpar='Parpar',
		                     Pctllabel='Parlabel',
		                     Pctlchan='Parchan',
		                     Pctlhelptext='Parhelptext',
		                     Pctlfontsize='Parfontsize')

	def GetValue(self):
		raise NotImplementedError()

	def SetValue(self, value):
		raise NotImplementedError()
