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
		initIOTemplate(d.op('input_template'))
		initIOTemplate(d.op('output_template'))
		d.op('input_replicator').par.recreateall.pulse()
		d.op('output_replicator').par.recreateall.pulse()
		self.AttachAllInputs()

	def BuildCCTable(self, dat, buttons, sliders):
		dat.clear()
		dat.appendRow(['ctrl', 'cc'])
		for row in buttons.rows() + sliders.rows():
			cc = int(str(row[1])[3:5], 16) + 1
			dat.appendRow([row[0], cc])

	def BuildIOTable(self, dat):
		dat.clear()
		dat.appendRow(['type', 'path', 'chans', 'ctrls', 'ccs'])
		mappings = dat.inputs[0]
		cctbl = dat.inputs[1]
		addIOTypeRows(dat, mappings, cctbl, 'out', 'outpath')
		addIOTypeRows(dat, mappings, cctbl, 'in', 'inpath')

	def UpdateIOReplicants(self, replicator, template, ops):
		for c in ops:
			c.par.clone = replicator.par.master
			path = template[c.digits, 'path']
			c.par.Tgtop = path
			if c.op('attach_to_target') is not None:
				c.op('attach_to_target').run()

	def AttachAllInputs(self):
		for attach in self._comp.ops('input_[1-9]*/attach_to_target'):
			attach.run()

	def AddToCtrlTable(self, tbl):
		devname = self._comp.par.Devname
		devpath = self._comp.path
		for ctrl in self._comp.op('cc_table').col('ctrl')[1:]:
			key = devname + ':' + ctrl
			updateTableRow(tbl,
			               key,
			               {
			                "dev": devname,
			                "ctrl": ctrl,
			                "devpath": devpath
			               },
			               addMissing=True)
		pass

	@property
	def MappingsTable(self):
		return self._comp.op('set_mappings')

	@property
	def GroupsTable(self):
		return self._comp.op('set_groups')

	def UpdateGroup(self, group, inpath, outpath):
		grouptbl = self.GroupsTable
		if not inpath and not outpath:
			grouptbl.removeRow(group)
		else:
			updateTableRow(grouptbl,
			               group,
			               { "inpath": inpath, "outpath": outpath },
			               addMissing=True)

	def UpdateMapping(self, group, chan, ctrl):
		mappingtbl = self.MappingsTable
		row = getMappingRow(mappingtbl, group, chan)
		if not ctrl:
			if row is not None:
				mappingtbl.deleteRow(row)
		else:
			if row is not None:
				mappingtbl[row, 'ctrl'] = ctrl
			else:
				mappingtbl.appendRow([group, chan, ctrl])

def getMappingRow(mappings, group, chan):
	for i in range(1, mappings.numRows):
		if mappings[i, 'group'] == group and mappings[i, 'chan'] == chan:
			return i

def initIOTemplate(comp):
	page = comp.appendCustomPage('Midi IO')
	page.appendCHOP('Tgtop', label='Target CHOP')

def addIOTypeRows(dat, mappings, cctbl, typeName, pathCol):
	paths = {x.val for x in mappings.col(pathCol)[1:]}
	for path in paths:
		ctrls = getVals(mappings, pathCol, path, 'ctrl')
		chans = getVals(mappings, pathCol, path, 'chan')
		ccs = ['ch1c' + cctbl[x, 'cc'].val for x in ctrls]
		dat.appendRow([
			typeName,
			path,
			' '.join(chans),
			' '.join(ctrls),
			' '.join(ccs)
		])

def getVals(mappings, matchCol, matchVal, field):
	results = []
	for i in range(1, mappings.numRows):
		if mappings[i, matchCol] == matchVal:
			results.append(mappings[i, field].val)
	return results
