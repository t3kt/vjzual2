setattrs = mod.vjz_util.setattrs

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
