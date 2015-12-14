try:
	import vjz_util as util
except ImportError:
	import vjz.util as util

setattrs = util.setattrs
setexpr = util.setexpr

# def setParentModuleHighlight(comp, highlight):
# 	m = comp.ext.vjzmod if comp and 'vjzmod' in comp.ext else None
# 	if not m or 'Modhighlight' not in m.par:
# 		return
# 	m.par.Modhighlight = highlight

class DataNode:
	def __init__(self, comp):
		self.comp = comp
		comp.tags.add('vjznode')

	def Initialize(self):
		n = self.comp
		page = n.appendCustomPage('Data Node')
		setattrs(page.appendStr('Nodeid', label='Node ID')[0],
		         default='node1')
		setattrs(page.appendStr('Nodelabel', label='Node Label')[0],
		         default='node 1')
		setattrs(page.appendToggle('Nodehasvideo', label='Has Video')[0],
		         default=True)
		page.appendTOP('Nodevideo', label='Video')
		setattrs(page.appendToggle('Nodehasaudio', label='Has Audio')[0],
		         default=True)
		page.appendCHOP('Nodeaudio', label='Audio')
		setattrs(page.appendToggle('Nodehasctrl', label='Has Control')[0],
		         default=False)
		page.appendCHOP('Nodectrl', label='Control')
		page.appendStr('Nodectrlchans', label='Control Channels')
		page.appendToggle('Nodehidden', label='Hidden')

		page.sort('Nodeid', 'Nodelabel',
		          'Nodehasvideo', 'Nodevideo',
		          'Nodehasaudio', 'Nodeaudio',
		          'Nodehasctrl', 'Nodectrl', 'Nodectrlchans',
		          'Nodehidden')

		self.UpdateDataParStates()

	def UpdateDataParStates(self):
		n = self.comp
		n.par.Nodevideo.enable = n.par.Nodehasvideo
		n.par.Nodeaudio.enable = n.par.Nodehasaudio
		n.par.Nodectrl.enable = n.par.Nodehasctrl
		n.par.Nodectrlchans.enable = n.par.Nodehasctrl

