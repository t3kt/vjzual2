__author__ = 'tekt'

print('module.py initializing')

if False:
	import vjz.util as util
else:
	import vjz_util as util

setattrs = util.setattrs
setexpr = util.setexpr
setParExprs = util.setParExprs
setParValues = util.setParValues

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
		util.setattrs(page.appendMenu('Modparuimode', label='Parameter UI Mode')[0],
		              menuNames=['ctrl', 'midiedit'],
		              menuLabels=['Controls', 'Edit MIDI'])
		page.appendToggle('Modhidden', label='Hide Module')
		page.appendToggle('Modhighlight', label='Highlight Module')
		self.UpdateHeight()
		outnode = m.op('out_node')
		if outnode is not None:
			setParExprs(outnode,
			            Nodeid="ext.vjzmod.par.Modname + ':wet'",
			            Nodelabel="ext.vjzmod.par.Moduilabel + ' (wet)'",
			            Nodehidden="ext.vjzmod.path.startswith('/_/components/')")
			setattrs(outnode.par,
			         Nodehasaudio=m.op('wet_audio') is not None,
			         Nodehasvideo=m.op('wet_video') is not None,
			         Nodehasctrl=False)
			setattrs(outnode.par,
			         Nodevideo='wet_video' if m.op('wet_video') else '',
			         Nodeaudio='wet_audio' if m.op('wet_audio') else '')

	@property
	def HeaderHeight(self):
		m = self._comp
		if m.par.Modcollapsed:
			return 20
		return 40

	@property
	def BodyHeight(self):
		m = self._comp
		if m.par.Modcollapsed:
			return 0
		bodypanel = m.op('bodypanel')
		if not bodypanel:
			return 60
		return VjzModule.GetVisibleCOMPsHeight(
			[c.owner for c in bodypanel.outputCOMPConnectors[0].connections])

	@staticmethod
	def GetVisibleCOMPsHeight(ops):
		h = 0
		for o in ops:
			if not o.isPanel or not o.par.display:
				continue
			h += o.par.h
		return h

	def UpdateHeight(self):
		m = self._comp
		if not m.par.Modautoheight:
			return
		bodyheight = self.BodyHeight
		m.op('bodypanel').par.h = bodyheight
		m.par.h = self.HeaderHeight + bodyheight

	def UpdateSolo(self):
		m = self._comp
		solo = m.par.Modsolo.eval()
		if solo and m.op('./out_node'):
			for mpath in m.op(m.var('moduletbl')).col('path')[1:]:
				othermod = m.op(mpath)
				if othermod is not m:
					othermod.par.Modsolo = False
			nodeId = m.op('./out_node').par.Nodeid.eval()
		else:
			nodeId = m.op(m.var('masteroutnode')).par.Nodeid.eval()
		print('updating master output to node id: ' + nodeId)
		m.op(m.var('mainoutselector')).SetSelectedNode(nodeId)

	@property
	def PresetsTable(self):
		return self._comp.op('local/preset_values')

	@property
	def PresetsDict(self):
		return self._comp.fetch('presets', {}, search=False, storeDefault=True)

	@PresetsDict.setter
	def PresetsDict(self, presets):
		self._comp.store('presets', presets)

	def GetValuesForPreset(self):
		return {p.name: p.eval() for p in self._comp.pars('Mpar*')}

	def SetValuesFromPreset(self, values):
		util.setPars(self._comp, **values)

	def LoadPreset(self, index):
		values = self.PresetsDict.get(str(index), None)
		if not values:
			print('LoadPreset', index, 'preset not found')
			return
		print('LoadPreset', index, 'values:', values)
		self.SetValuesFromPreset(values)

	def SavePreset(self, index):
		values = self.GetValuesForPreset()
		print('SavePreset', index, 'values:', values)
		self.PresetsDict[str(index)] = values

	def DoesPresetExist(self, index):
		return str(index) in self.PresetsDict

	# def GetSelectors(self):
	# 	m = self._comp
	# 	return [s for s in m.ops('*_selector') if hasattr(s.par, 'Selnodeid')]
	#
	# def GetSelectorValues(self):
	# 	vals = {}
	# 	for s in self.GetSelectors():
	# 		vals[s.name] = s.par.Selnodeid.eval()

	# def SetSelectorValues(self, values):
	# 	for selecto

	def GetStateDict(self):
		m = self._comp
		state = {
			'name': m.par.Modname.eval(),
			'path': m.path,
		}
		if m.par.Modbypass.eval():
			state['bypass'] = True
		params = self.GetValuesForPreset()
		if params:
			state['params'] = params
		presets = self.PresetsDict
		if presets:
			state['presets'] = presets
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
			self.PresetsDict = presets

class ModuleShell:
	def __init__(self, shell):
		self.shell = shell

	def Initialize(self):
		shell = self.shell
		page = shell.appendCustomPage('Module Shell')
		setattrs(page.appendToggle('Showcollapsebtn', label='Show Collapse Button')[0],
		         default=True)
		setattrs(page.appendToggle('Showsolobtn', label='Show Solo Button')[0],
		         default=True)
		setattrs(page.appendToggle('Showbypassbtn', label='Show Bypass Button')[0],
		         default=True)
		setattrs(page.appendToggle('Showpresetsbtn', label='Show Presets Button')[0],
		         default=True)
		setattrs(page.appendToggle('Showadvancedbtn', label='Show Advanced Button')[0],
		         default=True)
		setattrs(page.appendToggle('Showviewersbtn', label='Show Viewers Button')[0],
		         default=True)
		setattrs(page.appendToggle('Showparuimode', label='Show Par UI Mode Menu')[0],
		         default=True)
		shell.parent().par.crop = 'on'
		for init in shell.ops('*/init'):
			init.run()


def copyPresets(m):
	table = m.op('local/preset_values')
	if table.numRows < 2:
		return
	keys = [x.val for x in table.row(0)]
	presets = {}
	for i in range(1, table.numRows):
		presets[str(i)] = {key: table[i, key] for key in keys}
	m.PresetsDict = presets
