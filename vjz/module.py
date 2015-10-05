__author__ = 'tekt'

if False:
	import vjz.util as util
else:
	import vjz_util as util

setattrs = util.setattrs
setexpr = util.setexpr

class VjzModule:
	def __init__(self, comp):
		self._comp = comp

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
		minheight = int(var('modcollapsedheight'))
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

	@property
	def PresetsTable(self):
		return self._comp.op('local/preset_values')

	def GetValuesForPreset(self):
		return {p.name: p.eval() for p in self._comp.pars('Mpar*')}

	def SetValuesFromPreset(self, values):
		setattrs(self._comp.par, **values)

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