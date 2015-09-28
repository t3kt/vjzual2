from vjz_params import ParControl
import vjz_util as util

class ParRadioButtons(ParControl):
	def __init__(self, comp):
		ParControl.__init__(self, comp)

	def Initialize(self):
		ParControl.Initialize(self)
		page = self.GetParControlPage()
		

