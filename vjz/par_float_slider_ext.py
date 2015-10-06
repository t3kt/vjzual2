from vjz_params import ParControl
import vjz_util as util

setattrs = util.setattrs
overrideRows = util.overrideRows

class ParFloatSlider(ParControl):
	def __init__(self, comp):
		ParControl.__init__(self, comp)

	def Initialize(self):
		ParControl.Initialize(self)
		self._comp.par.top = './bg'
		self._comp.par.chop = './inputval'

	def PullValue(self):
		self._PullIntoPanelValue('u')

class ParFloatSlider_2(ParControl):
	def __init__(self, comp):
		ParControl.__init__(self, comp)

	def Initialize(self):
		ParControl.Initialize(self)
		s = self._comp
		page = self.GetParControlPage()
		setattrs(page.appendMenu('Pctlsliderstyle', label='Slider Style')[0],
		         menuNames=['std', 'xfade'],
		         menuLabels=['Standard', 'X-Fade'])
		util.overrideRows(s.op('slider/define'),
		                  font_size='`par("../../../Pctlfontsize")`',
		                  label='`pars("../../../Pctllabel")`',
		                  channelname='`pars("../../../Pctlchan")`',
		                  type='`pars("../../../Pctlsliderstyle")`',
		                  lower_range='`chop("../../par_attrs/normMin")`',
		                  upper_range='`chop("../../par_attrs/normMax")`',
		                  lower_clamp='`chop("../../par_attrs/clampMin")`',
		                  upper_clamp='`chop("../../par_attrs/clampMax")`')

	def PullValue(self):
		p = self.TargetPar
		if p is not None:
			self._comp.op('slider/set').run(p.eval())