__author__ = 'tekt'

print('module.py initializing')

import json

if False:
	import vjz.util as util
else:
	import vjz_util as util

setattrs = util.setattrs
setexpr = util.setexpr

class VjzModule:
	def __init__(self, comp):
		util.DBGLOG('%s\tModule constructor\t%r' % (comp.path, type(self)))
		self._comp = comp
		comp.tags.add('vjzmod')

	def GetModulePage(self):
		return self._comp.appendCustomPage('VjzModule')

	def GetModParamsPage(self):
		return self._comp.appendCustomPage('Modparams')

	def Initialize(self):
		util.DBGLOG('%s\tModule Initialize\t%r' % (self._comp.path, type(self)))
		m = self._comp
		m.par.inshortcut = 'vjzmod'
		page = self.GetModulePage()
		page.appendStr('Modname', label='Module Name')
		page.appendStr('Moduilabel', label='UI Label')
		page.appendToggle('Modbypass', label='Bypass')
		page.appendToggle('Modsolo', label='Solo')
		page.appendToggle('Modshowviewers', label='Show Viewers')
		page.appendToggle('Modcollapsed', label='Collapse')
		page.appendToggle('Modshowadvanced', label='Show Advanced')
		setattrs(page.appendToggle('Modautoheight', label='Auto Height'),
		         default=True)
		page.appendToggle('Modhasadvanced', label='Has Advanced Params')
		page.appendToggle('Modhasviewers', label='Has Viewers')
		util.setattrs(page.appendStr('Moduimode', label='UI Mode'),
					default='ctrl')
		page.appendToggle('Modhidden', label='Hide Module')
		page.appendToggle('Modhighlight', label='Highlight Module')
		self.UpdateHeight()

	@property
	def HeaderHeight(self):
		m = self._comp
		if m.par.Modcollapsed:
			return 24
		return 44

	@property
	def BodyHeight(self):
		m = self._comp
		if m.par.Modcollapsed:
			return 0
		bodypanel = m.op('bodypanel')
		if not bodypanel:
			return 60
		return util.GetVisibleChildCOMPsHeight(bodypanel)

	@property
	def MappingsHeight(self):
		m = self._comp
		if m.par.Modcollapsed:
			return 0
		mappings = m.op('midi_mappings')
		return mappings.par.h.eval() if mappings else 60

	@property
	def PresetsHeight(self):
		m = self._comp
		if m.par.Modcollapsed:
			return 0
		presetspanel = m.op('presets')
		return presetspanel.par.h.eval() if presetspanel else 60

	@staticmethod
	@util.deprecatedMethod
	def GetVisibleCOMPsHeight(ops):
		return util.GetVisibleCOMPsHeight(ops)

	def UpdateHeight(self):
		m = self._comp
		if not m.par.Modautoheight:
			return
		if m.par.Moduimode == 'midiedit':
			bodyheight = self.MappingsHeight
		elif m.par.Moduimode == 'presets':
			bodyheight = self.PresetsHeight
		else:
			bodyheight = self.BodyHeight
			m.op('bodypanel').par.h = bodyheight
		m.par.h = self.HeaderHeight + bodyheight

	def UpdateSolo(self):
		m = self._comp
		solo = m.par.Modsolo.eval()
		mainout = m.op(m.var('mainoutselector'))
		outnode = m.op('./out_node')
		if solo and outnode:
			for mpath in m.op(m.var('moduletbl')).col('path')[1:]:
				othermod = m.op(mpath)
				if othermod is not m:
					othermod.par.Modsolo = False
			nodeId = outnode.par.Nodeid.eval()
		elif mainout.par.Selnodeid == outnode.par.Nodeid:
			nodeId = m.op(m.var('masteroutnode')).par.Nodeid.eval()
		else:
			return
		print('updating master output to node id: ' + nodeId)
		mainout.par.Selnodeid = nodeId

	def GetValuesForPreset(self):
		return {p.name: p.eval() for p in self._comp.pars('Mpar*') if p.mode == ParMode.CONSTANT and not p.isOP}

	def SetValuesFromPreset(self, values):
		for name in values:
			p = getattr(self._comp.par, name, None)
			if p is not None:
				util.setParValue(p, values[name])
			else:
				print(self._comp.par.Modname + ': skipping missing param ' + name)

	def _GetPresetNameAndDataPars(self, i):
		name = getattr(self._comp.par, 'Preset%dname' % i, None)
		data = getattr(self._comp.par, 'Preset%ddata' % i, None)
		return name, data

	def _GetPresetsDict(self):
		presets = {}
		for i in range(1, 9):
			namePar, dataPar = self._GetPresetNameAndDataPars(i)
			if namePar is None or dataPar is None:
				continue
			name = namePar.eval()
			data = dataPar.eval()
			if not name or not data:
				continue
			presets[i] = {
				'name': name,
				'values': json.loads(data)
			}
		return presets

	def _LoadPresetsDict(self, presets):
		for i in range(1, 9):
			namePar, dataPar = self._GetPresetNameAndDataPars(i)
			preset = presets.get(i, {})
			# convert old-style preset dicts
			if preset and 'name' not in preset:
				preset = {'values': preset}
			namePar.val = preset.get('name', '')
			vals = preset.get('values')
			dataPar.val = json.dumps(vals) if vals else ''

	def GetStateDict(self):
		m = self._comp
		state = {
			'name': m.par.Modname.eval(),
			'label': m.par.Moduilabel.eval(),
			'path': m.path,
		}
		if m.par.Modbypass.eval():
			state['bypass'] = True
		params = self.GetValuesForPreset()
		if params:
			state['params'] = params
		presets = self._GetPresetsDict()
		if presets:
			state['presets'] = presets
		mappings = m.fetch('midiMappings', {}, search=False)
		mappings = {
			parName: mapping for (parName, mapping) in mappings.items() if mapping.get('midictl')
		}
		if mappings and '' in mappings:
			del mappings['']
		if mappings:
			state['mappings'] = mappings
		return state

	def LoadStateDict(self, state):
		m = self._comp
		print('%s loading state dict %r' % (m.path, state))
		m.par.Modbypass = state.get('bypass', False)
		params = state.get('params', None)
		if params:
			self.SetValuesFromPreset(params)
		presets = state.get('presets', None)
		if presets:
			self._LoadPresetsDict(presets)
		mappings = state.get('mappings', None)
		if mappings:
			m.store('midiMappings', mappings)


def copyPresets(m):
	table = m.op('local/preset_values')
	if table.numRows < 2:
		return
	keys = [x.val for x in table.row(0)]
	presets = {}
	for i in range(1, table.numRows):
		presets[str(i)] = {key: table[i, key] for key in keys}
	m.PresetsDict = presets
