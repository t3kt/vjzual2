try:
	from vjz_module import VjzModule
except ImportError:
	from vjz.module import VjzModule

import vjz_util as util
setattrs = util.setattrs

from math import floor

NUM_PARS=8

class MultiDelayModule(VjzModule):
	def __init__(self, comp):
		VjzModule.__init__(self, comp)

	def Initialize(self):
		VjzModule.Initialize(self)
		m = self._comp
		page = self.GetModParamsPage()
		page.appendFloat('Mparlevel', label='Level')
		setattrs(page.appendInt('Mparcachesize', label='Cache Size')[0],
			normMin=1,
			normMax=128,
			min=1,
			clampMin=True,
			default=32)

		setattrs(page.appendFloat('Mparlength', label='Master Length')[0],
			default=1)

		for i in range(1, NUM_PARS+1):
			pg = m.appendCustomPage('Modpartap' + str( floor((i-1)/2)+1))
			parprefix = 'Mpartap' + str(i+1)
			lblprefix = 'Tap ' + str(i+1) + ' '
			setattrs(pg.appendToggle(parprefix + 'active', label=lblprefix+'Active')[0],
				default=True)
			setattrs(pg.appendFloat(parprefix + 'length', label=lblprefix+'Length')[0],
				min=0, #redundant but helpful
				max=1,
				clampMin=True,
				clampMax=True)

			setattrs(pg.appendFloat(parprefix + 'alpha', label=lblprefix+'Alpha')[0],
				min=0, #redundant but helpful
				max=1,
				clampMin=True,
				clampMax=True,
				default=1)
			setattrs(pg.appendFloat(parprefix + 'filterhue', label=lblprefix+'Color Filter Hue')[0],
				normMax=1)
			pg.appendFloat(parprefix + 'filtersat', label=lblprefix+'Color Filter Amount')
			pg.appendToggle(parprefix + 'filteron', label=lblprefix+'Color Filter Enabled')

		self.UpdateTapParStates()

		for init in m.ops('shell/init', 'overlay/init', '*_param/init', 'tap*/init'):
			init.run()

	def UpdateTapParStates(self):
		m = self._comp
		for i in range(1, NUM_PARS+1):
			enabled = getattr(m.par, 'Mpartap%dactive' % i)
			self.ToggleTapPars(i, enabled.eval())

	def ToggleTapPars(self, i, enable):
		m = self._comp
		for suffix in ('length', 'alpha', 'filterhue', 'filtersat', 'filteron'):
			p = getattr(m.par, 'Mpartap%d%s' % (i, suffix))
			p.enable = enable
