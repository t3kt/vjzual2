setattrs = mod.vjz_util.setattrs
setexpr = mod.vjz_util.setexpr
overrideRows = mod.vjz_util.overrideRows

class MidiMapping:
	def __init__(self, comp):
		self._comp = comp

	def Initialize(self):
		m = self._comp
		page = m.appendCustomPage('MIDI Mapping')
		page.appendStr('Mapid', label='Mapping ID')
		page.appendStr('Mapchan', label='Channel Name')
		page.appendMenu('Mapctrl', label='Control')
		setattrs(page.appendToggle('Mapenabled', label='Enabled')[0],
		         default=True)

		m.tags.add('midimapping')

		setexpr(m.op('enabled_button').par.Pctlop, 'me.parent()')
		setattrs(m.op('enabled_button').par,
		         Pctlpar='Mapenabled',
		         Pctlchan='enabled',
		         Pctlhelptext='disable mapping',
		         Pctloffhelptext='enable mapping')

		setexpr(m.op('ctrl_menu').par.Pctlop, 'me.parent()')
		setattrs(m.op('ctrl_menu').par,
		         Pctlpar='Mapctrl',
		         Pctlhelptext='control mapping',
		         Pctllistsize=15,
		         Pctlhidebtn=True)
		page.sort('Mapid', 'Mapchan', 'Mapctrl', 'Mapenabled')

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

	@property
	def MappedDev(self):
		info = self._comp.op('selected_ctrl')
		if info.numRows < 2:
			return None
		return info[1, 'dev']

	@property
	def MappedCtrl(self):
		info = self._comp.op('selected_ctrl')
		if info.numRows < 2:
			return None
		return info[1, 'ctrl']
