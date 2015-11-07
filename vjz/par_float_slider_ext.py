if False:
	from vjz.params import ParControl
else:
	from vjz_params import ParControl
if False:
	import vjz.util as util
else:
	import vjz_util as util
from numpy import interp

class ParFloatSlider(ParControl):
	def __init__(self, comp):
		ParControl.__init__(self, comp)
		self.ParNormMin = tdu.Dependency(0)
		self.ParNormMax = tdu.Dependency(1)
		self.ParDefault = tdu.Dependency(0)

	def Initialize(self):
		ParControl.Initialize(self)
		self._comp.par.top = './bg'
		self._comp.par.chop = './inputval'
		self.UpdateParSettings()

	def UpdateParSettings(self):
		p = self.TargetPar
		if p is not None:
			self.ParNormMin.val = p.normMin
			self.ParNormMax.val = p.normMax
			self.ParDefault.val = p.default

	def PullValue(self):
		p = self.TargetPar
		if p is not None:
			if p.mode == ParMode.CONSTANT:
				self._comp.panel.u = p.normVal
			else:
				raw = p.eval()
				scaled = interp(raw, [p.normMin, p.normMax], [0.0, 1.0])
				self._comp.panel.u = scaled
