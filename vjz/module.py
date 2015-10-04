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
