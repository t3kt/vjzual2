setattrs = mod.vjz_util.setattrs
overrideRows = mod.vjz_util.overrideRows

class MidiMapping:
	def __init__(self, comp):
		self._comp = comp

	def Initialize(self):
		m = self._comp
		page = m.appendCustomPage('MIDI Mapping')
		page.appendStr('Mapgroup', label='Group Name')
		page.appendStr('Mapchan', label='Channel Name')
		page.appendMenu('Mapctrl', label='Control')
		setattrs(page.appendToggle('Mapenabled', label='Enabled')[0],
		         default=True)

		m.tags.add('midimapping')

		self.UpdateCtrlMenu()

		for init in m.ops('ctrl_menu/init', 'enabled_button/init'):
			init.run()

	def UpdateCtrlMenu(self):
		m = self._comp
		ctrls = m.op(m.var('midictrls'))
		ctrlIds = [x.val for x in ctrls.col('id')[1:]]
		setattrs(m.par.Mapctrl,
		         menuNames=['none'] + ctrlIds,
		         menuLabels=['--'] + ctrlIds)

