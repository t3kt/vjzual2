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
		m.op('update_tap_par_states').par.active = False
		page = self.GetModParamsPage()
		page.appendFloat('Mparlevel', label='Level')
		setattrs(page.appendInt('Mparcachesize', label='Cache Size')[0],
			normMin=1,
			normMax=128,
			min=1,
			clampMin=True,
			default=32)
		compopts = op(var('compositemenuopts'))
		setattrs(page.appendMenu('Mparoperand', label='Composite Operator')[0],
			menuNames=compopts.col('name')[1:],
			menuLabels=compopts.col('label')[1:])

		setattrs(page.appendFloat('Mparlength', label='Master Length')[0],
			default=1)

		for i in range(0, NUM_PARS):
			pg = m.appendCustomPage('Modpartap' + str( floor(i/2)+1))
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

		setattrs(
			[
				page.appendMenu('Mparlengthmode', label='Tap Length Mode')[0],
			    page.appendMenu('Mparalphamode', label='Tap Alpha Mode')[0]
			],
			menuNames=['individual', 'linear'],
			menuLabels=['Individual Settings', 'Linear Range'])
		page.appendFloat('Mparlengthrange', label='Tap Length Range', size=2)
		m.par.Mparlengthrange1.default = 0
		m.par.Mparlengthrange2.default = 1
		page.appendFloat('Mparalpharange', label='Tap Alpha Range', size=2)
		m.par.Mparalpharange1.default = 1
		m.par.Mparalpharange2.default = 0

		self.UpdateTapParStates()

		for init in m.ops('shell/init', 'overlay/init', '*_param/init', 'tap*/init'):
			init.run()
		m.op('update_tap_par_states').par.active = True

	def UpdateTapParStates(self):
		m = self._comp
		lengthmode = m.par.Mparlengthmode.eval()
		alphamode = m.par.Mparalphamode.eval()
		for i in range(1, NUM_PARS+1):
			enabled = getattr(m.par, 'Mpartap%dactive' % i).eval()
			self.ToggleTapPars(i, enabled and alphamode == 'individual',
			                   (
			                   'alpha',
			                   ))
			self.ToggleTapPars(i, enabled and lengthmode == 'individual',
			                   (
			                   'length',
			                   ))
			self.ToggleTapPars(i, enabled,
			                   (
			                   'filterhue', 'filtersat', 'filteron'
			                   ))

	def ToggleTapPars(self, i, enable, names):
		#print('ToggleTapPars', {"i":i, "enable":enable, "names":names, "pars":self.GetTapPars(i, names)})
		for p in self.GetTapPars(i, names):
			p.enable = enable

	def GetTapPars(self, i, names):
		return self._comp.pars(*['Mpartap%d%s' % (i, name) for name in names])

class MultiDelayTap:
	def __init__(self, comp):
		self._comp = comp

	def Initialize(self):
		t = self._comp
		page = t.appendCustomPage('Delay Tap')

		page.appendTOP('Cache', label='Cache TOP')
		page.appendCHOP('Audioop', label='Audio CHOP')

		setattrs(page.appendFloat('Length', label='Tap Length')[0],
			min=0, #redundant but helpful
			max=1,
			clampMin=True,
			clampMax=True)

		setattrs(page.appendFloat('Alpha', label='Tap Alpha')[0],
			min=0, #redundant but helpful
			max=1,
			clampMin=True,
			clampMax=True,
			default=1)
		setattrs(page.appendFloat('Filterhue', label='Color Filter Hue')[0],
			normMax=1)
		page.appendFloat('Filtersat', label='Color Filter Amount')
		page.appendToggle('Filteron', label='Color Filter Enabled')
		page.appendFloat('Audiomaxdelay', label='Max Audio Delay')
		page.appendFloat('Audiodelay', label='Audio Delay')
		page.appendFloat('Audiolevel', label='Audio Level')

		setattrs(page.appendToggle('Active', label='Active')[0],
			default=True)

		page.sort('Cache', 'Active',
				 'Length', 'Alpha',
				 'Filteron', 'Filtersat', 'Filterhue')
