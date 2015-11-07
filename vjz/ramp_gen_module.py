try:
	from vjz_module import VjzModule
except ImportError:
	from vjz.module import VjzModule

try:
	import vjz_util as util
except ImportError:
	import vjz.util as util

setattrs = util.setattrs
evalPars = util.evalPars

class RampGenModule(VjzModule):
	def __init__(self, comp):
		VjzModule.__init__(self, comp)

	def Initialize(self):
		VjzModule.Initialize(self)
		m = self._comp
		page = self.GetModParamsPage()
		ramp = m.op('ramp')
		setattrs(page.appendMenu('Mparramptype', label='Ramp Type'),
		         menuNames=ramp.par.type.menuNames,
		         menuLabels=ramp.par.type.menuLabels,
		         default='horizontal')
		setattrs(page.appendFloat('Mparphase', label='Phase'),
		         normMin=-1,
		         normMax=1)
		setattrs(page.appendFloat('Mparperiod', label='Period'),
		         normMax=3,
		         default=1)
		setattrs(page.appendMenu('Mparextendleft', label='Extend Left'),
		         menuNames=ramp.par.extendleft.menuNames,
		         menuLabels=ramp.par.extendleft.menuLabels,
		         default=ramp.par.extendleft.default)
		setattrs(page.appendMenu('Mparextendright', label='Extend Right'),
		         menuNames=ramp.par.extendright.menuNames,
		         menuLabels=ramp.par.extendright.menuLabels,
		         default=ramp.par.extendright.default)
		setattrs(page.appendMenu('Mparinterp', label='Interpolate'),
		         menuNames=ramp.par.interp.menuNames,
		         menuLabels=ramp.par.interp.menuLabels,
		         default='linear')
		page.appendRGBA('Mparstartcolor', label='Start Color')
		m.par.Mparstartcolorr.default = 0
		m.par.Mparstartcolorg.default = 0
		m.par.Mparstartcolorb.default = 0
		m.par.Mparstartcolora.default = 1
		page.appendRGBA('Mparendcolor', label='End Color')
		m.par.Mparendcolorr.default = 1
		m.par.Mparendcolorg.default = 1
		m.par.Mparendcolorb.default = 1
		m.par.Mparendcolora.default = 1
		setattrs(page.appendMenu('Mparkeymode', label='Ramp Key Mode'),
		         menuNames=['simple', 'midpoint', 'midbar'],
		         menuLabels=['Two Keys', 'Midpoint', 'Midbar'],
		         default='simple')
		setattrs(page.appendFloat('Mparmidpos', label='Middle Position'),
		         normMin=0, min=0, clampMin=True,
		         normMax=1, max=1, clampMax=True,
		         default=0.5)
		page.appendToggle('Mparmidowncolor', label='Middle Has Own Color')
		setattrs(page.appendFloat('Mparmidcolorratio', label='Middle Color Ratio'),
		         normMin=0, min=0, clampMin=True,
		         normMax=1, max=1, clampMax=True,
		         default=0.5)
		page.appendRGBA('Mparmidcolor', label='Middle Color')
		m.par.Mparmidcolorr.default = 0.5
		m.par.Mparmidcolorg.default = 0.5
		m.par.Mparmidcolorb.default = 0.5
		m.par.Mparmidcolora.default = 1
		setattrs(page.appendFloat('Mparmidwidth', label='Middle Width'),
		         normMin=0,
		         normMax=0.5,
		         default=0.05)
		setattrs(page.appendFloat('Mparmidfadewidth', label='Middle Fade Width'),
		         normMin=0,
		         normMax=0.5,
		         default=0.05)
		page.appendToggle('Mparphaselfoon', label='Phase LFO On')
		setattrs(page.appendMenu('Mparphaselfowavetype', label='Phase LFO Type'),
		         menuNames=['sin', 'normal', 'tri', 'ramp', 'square', 'pulse'],
		         menuLabels=['Sine', 'Gaussian', 'Triangle', 'Ramp', 'Square', 'Pulse'],
		         default='sin')
		setattrs(page.appendFloat('Mparphaselfofreq', label='Phase LFO Frequency'),
		         normMin=-3, normMax=3, default=0.2)

		for init in m.ops('*/init'):
			init.run()

	def FillKeyTable(self, dat):
		dat.clear()
		m = self._comp
		dat.appendRow(['pos', 'r', 'g', 'b', 'a'])
		startcolor = evalPars(m.pars('Mparstartcolor[rgba]'))
		endcolor = evalPars(m.pars('Mparendcolor[rgba]'))
		keymode = m.par.Mparkeymode.eval()
		dat.appendRow([0] + startcolor)
		if keymode in ['midpoint', 'midbar']:
			if m.par.Mparmidowncolor:
				middlecolor = evalPars(m.pars('Mparmidcolor[rgba]'))
			else:
				ratio = m.par.Mparmidcolorratio.eval()
				middlecolor = util.interpLists(ratio, startcolor, endcolor)
			midpos = m.par.Mparmidpos.eval()
			if keymode == 'midpoint':
				dat.appendRow([midpos] + middlecolor)
			elif keymode == 'midbar':
				halfwidth = m.par.Mparmidwidth.eval() / 2
				fade = max(m.par.Mparmidfadewidth.eval(), 0.00001)
				dat.appendRow([util.clamp(midpos - halfwidth - fade, 0, 1)] + startcolor)
				dat.appendRow([util.clamp(midpos - halfwidth, 0, 1)] + middlecolor)
				dat.appendRow([util.clamp(midpos + halfwidth, 0, 1)] + middlecolor)
				dat.appendRow([util.clamp(midpos + halfwidth + fade, 0, 1)] + endcolor)
		dat.appendRow([1] + endcolor)
