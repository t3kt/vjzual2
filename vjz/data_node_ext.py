try:
	import vjz_util as util
except ImportError:
	import vjz.util as util

setattrs = util.setattrs
setexpr = util.setexpr
setParValues = util.setParValues
setParExprs = util.setParExprs
overrideRows = util.overrideRows

_nodeParMap = {
	"Nodehasvideo": "Nodevideo",
	"Nodehasaudio": "Nodeaudio",
	"Nodehasctrl": "Nodectrl"
}

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
		page.appendToggle('Nodehidden', label='Hidden')

		page.sort('Nodeid', 'Nodelabel',
		          'Nodehasvideo', 'Nodevideo',
		          'Nodehasaudio', 'Nodeaudio',
		          'Nodehasctrl', 'Nodectrl',
		          'Nodehidden')

		self.UpdateDataParStates()

	def UpdateDataParStates(self):
		n = self.comp
		for switchParName in _nodeParMap:
			switchPar = getattr(n.par, switchParName)
			sourcePar = getattr(n.par, _nodeParMap[switchParName])
			sourcePar.enable = switchPar.eval()

class DataSelector:
	def __init__(self, comp):
		self.comp = comp

	def Initialize(self):
		s = self.comp
		page = s.appendCustomPage('Data Selector')
		page.appendStr('Selnodeid', label='Selected Node ID')
		setattrs(page.appendToggle('Selreqvideo', label='Require Video')[0],
		         default=True)
		setattrs(page.appendToggle('Selreqaudio', label='Require Audio')[0],
		         default=False)
		setattrs(page.appendToggle('Selreqctrl', label='Require Control')[0],
		         default=False)
		page.appendStr('Selincludeid', label='Include ID Regexes')
		page.appendStr('Selexcludeid', label='Exclude ID Regexes')
		page.appendStr('Selincludepath', label='Include Path Regexes')
		page.appendStr('Selexcludepath', label='Exclude Path Regexes')
		setattrs(page.appendMenu('Selpreview', label='Preview Mode')[0],
		         menuNames=['video', 'audio', 'ctrl'],
		         menuLabels=['Video', 'Audio', 'Control'])
		page.appendToggle('Selpreviewon', label='Preview Enabled')
		setattrs(page.appendInt('Selpreviewheight', label='Preview Height'),
		         normMin=10,
		         normMax=200,
		         default=100)

		page.sort('Selnodeid',
		          'Selreqvideo', 'Selreqaudio', 'Selreqctrl',
		          'Selincludeid', 'Selexcludeid', 'Selincludepath', 'Selexcludepath',
		          'Selpreview', 'Selpreviewon', 'Selpreviewheight')

		setexpr(s.par.h, '20 + (me.par.Selpreviewheight if me.par.Selpreviewon else 0)')

		nodeList = s.op('node_drop_list')
		overrideRows(nodeList.op('define'),
		             displaylabel=0,
		             listitems=15)
		nodeListScript = nodeList.op('script')
		nodeListScript.python = True
		nodeListScript.text = 'me.parent(2).UpdateFromList()'

		setattrs(s.op('preview_mode').par,
		         Pctlop='..',
		         Pctlpar='Selpreview',
		         Pctllabel='',
		         Pctlfontsize=7,
		         Pctllistsize=3,
		         Pctlhidebtn=True)

		for init in s.ops('*/init'):
			init.run()

		self.UpdateFromList()

	def UpdateFromList(self):
		i = int(self.comp.op('node_drop_list/out1')[0, 1])
		self.SetSelectedNodeIndex(i)

	def SetSelectedNodeIndex(self, i):
		filteredNodes = self.comp.op('filtered_nodes')
		if i is None or i > filteredNodes.numRows - 1:
			return
		nodeCell = filteredNodes[i + 1, 'id']
		if nodeCell is not None:
			nodeId = nodeCell.val
			self.comp.par.Selnodeid = nodeId

	def SetSelectedNode(self, nodeId):
		filteredNodes = self.comp.op('filtered_nodes')
		nodeCell = filteredNodes[nodeId, 'id'] if nodeId else None
		if nodeCell is not None:
			i = nodeCell.row - 1
			self.comp.op('node_drop_list/set').run(i)
			#self.SetSelectedNodeIndex(i)