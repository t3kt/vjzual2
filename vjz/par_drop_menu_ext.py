from vjz_params import ParControl
import vjz_util as util

class ParDropMenu(ParControl):
	def __init__(self, comp):
		ParControl.__init__(self, comp)
	
	def Initialize(self):
		ParControl.Initialize(self)
		page = self.GetParControlPage()
		util.setattrs(page.appendInt('Pctllistsize', label='List Items')[0],
					  min=1,
					  normMin=1,
					  clampMin=1,
					  normMax=10,
					  default=5)
		page.appendToggle('Pctlhidebtn', label='Hide Button')
		util.overrideRows(self._comp.op('droplist/define'),
						  displaylabel=0,
						  font_size="`par(opparent($gadget, 0) + '/Pctlfontsize')`",
						  listitems="`par(opparent($gadget, 0) + '/Pctllistsize')`",
						  hidebtn="`par(opparent($gadget, 0) + '/Pctlhidebtn')`")
		p = self.TargetPar
		if p is not None:
			util.fillParamMenuOptionsTable(self._comp.op('menu_options'), p)

	def PullValue(self):
		p = self.TargetPar
		if p is not None:
			self._comp.op('droplist/set').run(p.menuIndex)
