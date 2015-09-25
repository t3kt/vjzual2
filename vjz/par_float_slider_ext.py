from vjz_params import ParControl
import vjz_util as util

class ParFloatSlider(ParControl):
	def __init__(self, comp):
		ParControl.__init__(self, comp)

	def Initialize(self):
		ParControl.Initialize(self)
		self._comp.par.top = './bg'
		self._comp.par.chop = './inputval'
	def PullValue(self):
		self._PullIntoPanelValue('u')
