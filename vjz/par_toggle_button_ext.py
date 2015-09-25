from vjz_params import ParControl
import vjz_util as util

class ParToggleButton(ParControl):
	def __init__(self, comp):
		ParControl.__init__(self, comp)

	def Initialize(self):
		ParControl.Initialize(self)
		self._comp.par.top = './bg'
		page = self.GetParControlPage()
		page.appendStr('Pctlontext', label='Button On Text')
		page.appendStr('Pctlofftext', label='Button Off Text')
		page.appendStr('Pctloffhelptext', label='Button Off Help Text')

	def PullValue(self):
		self._PullIntoPanelValue('state')
