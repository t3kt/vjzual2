__author__ = 'tekt'

if False:
	import vjz.util as util
else:
	import vjz_util as util

class ParControl:
	def __init__(self, comp):
		self._comp = comp
		self.Initialize()

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
		#print('ParControl pulling value', self, 'targetpar=', p, 'into', name)
		if p is not None:
			setattr(self._comp.panel, name, p.eval())

	def PushValue(self, value):
		p = self.TargetPar
		#print('ParControl pulling value', self, 'targetpar=', p)
		if p is not None:
			p.val = value

class VjzParam:
	def __init__(self, comp):
		self._comp = comp
		self.Initialize()

	def GetParamPage(self):
		return self._comp.appendCustomPage('VjzParam')

	def Initialize(self):
		self._comp.par.inshortcut = 'vjzpar'
		page = self.GetParamPage()
		page.appendOP('Parop', label='Target Operator')
		page.appendStr('Parpar', label='Target Parameter')
		page.appendStr('Parlabel', label='UI Label')
		page.appendStr('Parchan', label='Output Channel')
		page.appendStr('Parhelptext', label='Help Text')
		util.setattrs(page.appendInt('Parfontsize', label='Font Size')[0],
					  default=12, min=1, normMin=1, normMax=30, clampMin=True)