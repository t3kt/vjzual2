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
		self._comp = comp
		comp.tags.add('vjzmod')

	def GetModulePage(self):
		return self._comp.appendCustomPage('VjzModule')

	def GetModParamsPage(self):
		return self._comp.appendCustomPage('Modparams')

	def Initialize(self):
		self._comp.par.inshortcut = 'vjzmod'
		page = self.GetModulePage()
		page.appendStr('Modname', label='Module Name')
		page.appendStr('Moduilabel', label='UI Label')
		page.appendToggle('Modbypass', label='Bypass')
		page.appendToggle('Modsolo', label='Solo')
		page.appendToggle('Modshowviewers', label='Show Viewers')
		page.appendToggle('Modcollapsed', label='Collapse')
		page.appendToggle('Modshowadvanced', label='Show Advanced')
		minheight = int(float(var('modcollapsedheight')))
		fullheight = page.appendInt('Modfullheight', label='Full Height')[0]
		setattrs(fullheight,
			default= 200,
			min=minheight,
			normMin=minheight,
			clampMin=True,
			normMax=600)
		compactheight = page.appendInt('Modcompactheight', label='Compact Height')[0]
		setattrs(compactheight,
			default= 200,
			min= minheight,
			normMin= minheight,
			clampMin= True,
			normMax= 600)
		page.appendToggle('Modhasadvanced', label='Has Advanced Params')
		page.appendToggle('Modhasviewers', label='Has Viewers')
		setexpr(self._comp.par.h, 'op("./shell/mod_height")[0, 0]')
		util.setattrs(page.appendMenu('Modparuimode', label='Parameter UI Mode')[0],
		              menuNames=['ctrl', 'midiedit'],
		              menuLabels=['Controls', 'Edit MIDI'])
		page.appendToggle('Modhidden', label='Hide Module')

	@property
	def PresetsTable(self):
		return self._comp.op('local/preset_values')

	def GetValuesForPreset(self):
		return {p.name: p.eval() for p in self._comp.pars('Mpar*')}

	def SetValuesFromPreset(self, values):
		util.setPars(self._comp, **values)

	def LoadPreset(self, index):
		values = {}
		presets = self.PresetsTable
		for name in presets.col(0):
			values[name.val] = str(presets[name, index])
		if not presets or not values or index >= presets.numCols:
			print('LoadPreset', index, 'index out of range')
			return
		print('LoadPreset', index, 'values:', values)
		self.SetValuesFromPreset(values)

	def SavePreset(self, index):
		values = self.GetValuesForPreset()
		presets = self.PresetsTable
		if not presets or not values:
			return
		if index >= presets.numCols:
			presets.setSize(presets.numRows, index + 1)
		existingNames = {x.val for x in presets.col(0) if x.val}
		valueNames = set(values.keys())
		print('SavePreset', index, 'existing:', existingNames, 'values:', valueNames)
		allNames = existingNames.union(valueNames)
		for name in allNames:
			if not name:
				continue
			if not presets.row(name):
				presets.appendRow([name])
			if name in values:
				presets[name, index] = values[name]
			else:
				presets[name, index] = ''
		if presets[0, 0] == '':
			presets.deleteRow(0)

	def DoesPresetExist(self, index):
		presets = self.PresetsTable
		if not presets or presets.numRows == 0 or index >= presets.numCols:
			return False
		for row in range(presets.numRows):
			if presets[row, index] != '':
				return True
		return False

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
		setParExprs(shell.op('presets_button'),
		            display='parent().par.Showpresetsbtn')
		setParExprs(shell.ops('collapsed_button',
		                      'bypass_button',
		                      'solo_button',
		                      'viewers_button',
		                      'advanced_button',
		                      'par_ui_mode_menu'),
		            Pctlop='ext.vjzmod')
		setParValues(shell.op('collapsed_button'),
		             Pctlpar='Modcollapsed',
		             Pctlchan='collapsed',
		             Pctlhelptext='expand',
		             Pctloffhelptext='collapse',
		             Pctlontext='+',
		             Pctlofftext='-')
		setParExprs(shell.op('collapsed_button'),
		            display='parent().par.Showcollapsebtn')
		setParValues(shell.op('bypass_button'),
		             Pctlpar='Modbypass',
		             Pctlchan='bypass',
		             Pctlhelptext='bypass',
		             Pctloffhelptext='bypass',
		             Pctlontext='B',
		             Pctlofftext='B')
		setParExprs(shell.op('bypass_button'),
		            display='parent().par.Showbypassbtn')
		setParValues(shell.op('solo_button'),
		             Pctlpar='Modsolo',
		             Pctlchan='solo',
		             Pctlhelptext='solo',
		             Pctloffhelptext='solo',
		             Pctlontext='S',
		             Pctlofftext='S')
		setParExprs(shell.op('solo_button'),
		            display='parent().par.Showsolobtn')
		setParValues(shell.op('viewers_button'),
		             Pctlpar='Modshowviewers',
		             Pctlchan='showviewers',
		             Pctlhelptext='hide viewers',
		             Pctloffhelptext='show viewers',
		             Pctlontext='V',
		             Pctlofftext='V')
		setParExprs(shell.op('viewers_button'),
		            display='parent().par.Showviewersbtn')
		setParValues(shell.op('advanced_button'),
		             Pctlpar='Modshowadvanced',
		             Pctlchan='showadvanced',
		             Pctlhelptext='hide advanced params',
		             Pctloffhelptext='show advanced params',
		             Pctlontext='A',
		             Pctlofftext='A')
		setParExprs(shell.op('advanced_button'),
		            display='parent().par.Showadvancedbtn')
		setParValues(shell.op('par_ui_mode_menu'),
		             Pctlpar='Modparuimode',
		             Pctlchan='paruimode',
		             Pctlfontsize=7,
		             Pctllistsize=2,
		             Pctlhidebtn=True)
		setParExprs(shell.op('par_ui_mode_menu'),
		            display='parent().par.Showparuimode')
		setexpr(shell.op('presets').par.Presetmodule, "ext.vjzmod")
		shell.parent().par.crop = 'on'
		for init in shell.ops('*/init'):
			init.run()
