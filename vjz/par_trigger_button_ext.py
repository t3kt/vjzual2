from vjz_params import ParControl
import vjz_util as util

class ParTriggerButton(ParControl):
	def __init__(self, comp):
		ParControl.__init__(self, comp)

	def Initialize(self):
		ParControl.Initialize(self)
		self._comp.par.top = './bg'
		self._comp.par.buttontype = 'momentary'

	def PullValue(self):
		self._PullIntoPanelValue('state')

	def PushValue(self, *ignored):
		p = self.TargetPar
		if p is not None:
			p.pulse()
