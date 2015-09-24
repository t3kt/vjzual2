from vjz_params import ParControl
import vjz_util as util

class ParDropMenu(ParControl):
	def __init__(self, comp):
		ParControl.__init__(self, comp)
	
	def Initialize(self):
		ParControl.Initialize(self)
		self._comp.par.top = './bg'
		page = self.GetParControlPage()
		util.setattrs(page.appendInt('Pctllistsize', label='List Items')[0],
					  min=1,
					  normMin=1,
					  clampMin=1,
					  normMax=10,
					  default=5)
		util.overrideRows(self._comp.op('droplist/define'),
						  displaylabel=0,
						  font_size="`par(opparent($gadget, 0) + '/Pctlfontsize')`",
						  listitems="`par(opparent($gadget, 0) + '/Pctllistsize')`")