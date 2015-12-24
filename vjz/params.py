__author__ = 'tekt'

print('params.py initializing')

if False:
	import vjz.util as util
else:
	import vjz_util as util

class ParControl:
	def __init__(self, comp):
		util.DBGLOG('%s\tParControl constructor\t%r' % (comp.path, type(self)))
		self._comp = comp

	def GetParControlPage(self):
		return self._comp.appendCustomPage('ParCtrl')

	def Initialize(self):
		util.DBGLOG('%s\tParControl Initialize\t%r' % (self._comp.path, type(self)))
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
