setattrs = mod.vjz_util.setattrs
updateTableRow = mod.vjz_util.updateTableRow

class MidiDevice:
	def __init__(self, comp):
		self._comp = comp

	def Initialize(self):
		d = self._comp
		page = d.appendCustomPage('Midi Device')
		page.appendStr('Devname', label='Device Name')
		page.appendStr('Devlabel', label='Device Label')
		setattrs(page.appendInt('Devnum', label='Device Number')[0],
		         min=0, normMin=0, clampMin=True, normMax=16, default=1)
		setattrs(page.appendStr('Devtable', label='Device Table')[0],
		         default='/local/midi/device')
		if d.par.Devtable == '':
			d.par.Devtable = d.par.Devtable.default
		setattrs(page.appendToggle('Devenabled', label='Device Enabled')[0],
		         default=True)

	@property
	def MappingsTable(self):
		return self._comp.op('set_mappings')

	@property
	def GroupsTable(self):
		return self._comp.op('set_groups')

