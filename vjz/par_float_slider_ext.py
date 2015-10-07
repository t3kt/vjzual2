from vjz_params import ParControl
import vjz_util as util
from numpy import interp

class ParFloatSlider(ParControl):
	def __init__(self, comp):
		ParControl.__init__(self, comp)

	def Initialize(self):
		ParControl.Initialize(self)
		self._comp.par.top = './bg'
		self._comp.par.chop = './inputval'
		attrs = self._comp.op('set_par_attrs')
		attrs.clear()
		p = self.TargetPar
		if p is not None:
			attrs.appendChan('normMin').vals=[p.normMin]
			attrs.appendChan('normMax').vals=[p.normMax]
			attrs.appendChan('default').vals=[p.default]
		else:
			attrs.appendChan('normMin').vals=[0]
			attrs.appendChan('normMax').vals=[1]
			attrs.appendChan('default').vals=[0]

	def PullValue(self):
		p = self.TargetPar
		if p is not None:
			attrs = self._comp.op('par_attrs')
			raw = p.eval()
			scaled = interp(raw, [attrs['normMin'][0], attrs['normMax'][0]], [0.0, 1.0])
			self._comp.panel.u = scaled
