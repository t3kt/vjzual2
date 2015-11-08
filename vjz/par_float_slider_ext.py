if False:
	from vjz.params import ParControl
else:
	from vjz_params import ParControl
if False:
	import vjz.util as util
else:
	import vjz_util as util
from numpy import interp

setattrs = util.setattrs

class ParFloatSlider(ParControl):
	def __init__(self, comp):
		ParControl.__init__(self, comp)

	def Initialize(self):
		ParControl.Initialize(self)
		ctl = self._comp
		ctl.par.top = './bg'
		ctl.par.chop = './inputval'
		page = self.GetParControlPage()
		page.appendFloat('Pctlnormrange', label='Normalized Range', size=2)
		ctl.par.Pctlnormrange1.default = 0
		ctl.par.Pctlnormrange2.default = 1
		page.appendFloat('Pctlrange', label='Range', size=2)
		ctl.par.Pctlrange1.default = 0
		ctl.par.Pctlrange2.default = 1
		page.appendToggle('Pctlclampmin', label='Clamp Min')
		page.appendToggle('Pctlclampmax', label='Clamp Max')

	def PullValue(self):
		p = self.TargetPar
		ctl = self._comp
		if p is not None:
			if p.mode == ParMode.CONSTANT:
				ctl.panel.u = p.normVal
			else:
				raw = p.eval()
				scaled = interp(raw, [ctl.par.Pctlnormrange1, ctl.par.Pctlnormrange2], [0.0, 1.0])
				ctl.panel.u = scaled
