from numpy import interp
import json

def getTargetPane():
	return mod.vjz_util.GetActiveEditor()

def goTo(path):
	pane = getTargetPane()
	if not pane:
		return
	target = op(path)
	if not target:
		return
	pane.owner = target

def getSelected():
	pane = getTargetPane()
	if not pane:
		return
	selected= pane.owner.selectedChildren
	if not selected:
		selected = [pane.owner.currentChild]
	return selected

def _tryInit(o):
	if not o:
		return False
	if o.isDAT and o.name == 'init':
		init = o
	elif o.isCOMP:
		init = o.op('init')
	else:
		init = None
	if not init or not init.isDAT:
		return False
	try:
		ui.status = 'running initializer ' + init.path
		mod.vjz_util.DBGLOG('%s\tRUNNING INITIALIZER' % init.path)
		init.run()
	except Exception as e:
		print('INIT error [' + init.path + ']: ' + str(e))
	return True

def initSelectedOrContext():
	_doOnSelectedOrContext(_tryInit)

def _doOnSelectedOrContext(action):
	selected = getSelected()
	initedAny = False
	for o in selected:
		if action(o):
			initedAny = True
	if not initedAny:
		pane = getTargetPane()
		comp = pane.owner
		while comp:
			if action(comp):
				return
			comp = comp.parent()

def deletePars(o, *parNames):
	pars = o.pars(*parNames)
	for p in pars:
		p.destroy()

def setModParamEditModeExprs():
	params = getSelected()
	for p in params:
		if not hasattr(p.par, 'Paruimode'):
			print('setModParamEditModeExprs skipping', p)
			continue
		p.par.Paruimode.mode = ParMode.EXPRESSION
		p.par.Paruimode.expr = 'ext.vjzmod.par.Modparuimode'

# def _createRangeValGetter(startVal, endVal):
# 	return lambda i, n: interp(float(i), [0.0, float(n)-1.0], [startVal, endVal])
#
# def _setAttrsInOrder(objs, sortAttr, setAttr, calcVal=None, startVal=0.0, endVal=1.0):
# 	if calcVal is None:
# 		calcVal = _createRangeValGetter(startVal, endVal)
# 	if isinstance(sortAttr, str):
# 		sortAttrName = sortAttr
# 		sortAttr = lambda o: getattr(o, sortAttrName)
# 	sortedObjs = sorted(objs, key=sortAttr)
# 	if isinstance(setAttr, str):
# 		setAttrName = setAttr
# 		setAttr = lambda o, v: setattr(o, setAttrName, v)
# 	n = len(sortedObjs)
# 	for i in range(n):
# 		obj = sortedObjs[i]
# 		val = calcVal(i, n)
# 		setAttr(obj, val)

def setAlignOrderBy(sortAttrName, reverseDir):
	selected = getSelected()
	n = len(selected)
	selected = sorted(selected,
	                  key=lambda o: getattr(o, sortAttrName),
	                  reverse=reverseDir)
	for i in range(n):
		if hasattr(selected[i].par, 'order'):
			val = interp(float(i), [0, n-1], [0.0, 1.0])
			selected[i].par.order = val

def setAlignOrderByX():
	setAlignOrderBy('nodeX', False)

def setAlignOrderByY():
	setAlignOrderBy('nodeY', True)

def reloadPython():
	for name in ['vjz_util', 'vjz_params', 'vjz_module', 'vjz', 'vjz_core']:
		op('/local/modules/' + name).par.reload.pulse(1)

def destroyPars(parnames):
	selected = getSelected()
	print('destroyPars', parnames, selected)
	for o in selected:
		oPars = o.pars(*parnames)
		for p in oPars:
			if p.isCustom:
				p.destroy()

def addTags(tags):
	tags = set(tags)
	selected = getSelected()
	print('addTags', tags, selected)
	for o in selected:
		o.tags |= tags

def removeTags(tags):
	if len(tags) == 1 and tags[0] == '*':
		tags = None
	else:
		tags = set(tags)
	selected = getSelected()
	print('removeTags', tags if tags else '*', selected)
	for o in selected:
		if tags:
			o.tags -= tags
		else:
			o.tags.clear()

def _saveTox(comp):
	if not comp or not comp.isCOMP:
		return False
	toxfile = comp.par.externaltox.eval()
	if not toxfile:
		return False
	comp.save(toxfile)
	ui.status = 'Saved TOX %s to %s' % (comp.path, toxfile)
	return True

def saveToxSelectedOrContext():
	_doOnSelectedOrContext(_saveTox)

def _getMiddle(vals):
	low, high = min(vals), max(vals)
	return low + (high-low)/2

class NodeEdge:
	def __init__(self, attrName, calc):
		self.attrName = attrName
		self.calc = calc
	def get(self, op):
		return getattr(op, self.attrName)
	def set(self, op, val):
		setattr(op, self.attrName, val)
	def align(self, ops):
		vals = [self.get(o) for o in ops]
		newval = self.calc(vals)
		for o in ops:
			self.set(o, newval)

class DerivedNodeEdge(NodeEdge):
	def __init__(self, baseAttr, sizeAttr, calc):
		NodeEdge.__init__(self, baseAttr, calc)
		self.sizeAttr = sizeAttr
	def get(self, op):
		return getattr(op, self.attrName) + getattr(op, self.sizeAttr)
	def set(self, op, val):
		setattr(op, self.attrName, val - getattr(op, self.sizeAttr))

nodeEdges = {
	'left': NodeEdge('nodeX', min),
    'top': NodeEdge('nodeY', min),
    'center': NodeEdge('nodeCenterX', _getMiddle),
    'middle': NodeEdge('nodeCenterY', _getMiddle),
    'right': DerivedNodeEdge('nodeX', 'nodeWidth', max),
    'bottom': DerivedNodeEdge('nodeY', 'nodeHeight', max)
}

def align(dirName):
	selected = getSelected()
	if len(selected) < 2:
		return
	edge = nodeEdges[dirName]
	edge.align(selected)

def distribute(axis):
	if axis == 'x':
		attr = 'nodeX'
	else:
		attr = 'nodeY'
	selected = getSelected()
	n = len(selected)
	if n < 3:
		return
	vals = [getattr(o, attr) for o in selected]
	minVal, maxVal = min(vals), max(vals)
	selected = sorted(selected,
	                  key=lambda o: getattr(o, attr))
	for i in range(n):
		val = interp(float(i), [0, n-1], [minVal, maxVal])
		setattr(selected[i], attr, round(val))

def _setParValsUnlessExported(p, **parVals):
	for parName in parVals:
		par = getattr(p.par, parName, None)
		if par is None or par.mode == ParMode.EXPORT:
			return
		par.expr = ''
		par.val = parVals[parName]

def updateParSettings():
	params = getSelected()
	for p in params:
		if not p.isCOMP:
			continue
		clone = p.par.clone.eval()
		if clone is None:
			continue
		ptype = clone.path.replace('/_/components/', '')
		print('updating settings for par ', p.path, ' ptype=', ptype)
		if ptype in ['par_toggle_button', 'par_float_slider', 'par_drop_menu', 'bool_param', 'float_param', 'menu_param']:
			par = p.TargetPar
		elif ptype in ['par_toggle_button_2', 'par_float_slider_2', 'par_drop_menu_2']:
			targetOp = p.par.Pctlop.eval()
			parName = p.par.Pctlpar.eval()
			par = getattr(targetOp.par, parName, None) if targetOp else None
		elif ptype in ['bool_param_2', 'float_param_2', 'menu_param_2']:
			targetOp = p.par.Parop.eval()
			parName = p.par.Parpar.eval()
			par = getattr(targetOp.par, parName, None) if targetOp else None
		else:
			par = None
		if par is None:
			print('unable to get target par for path', p.path)
			continue
		if ptype in ['par_float_slider', 'par_float_slider_2']:
			_setParValsUnlessExported(p,
				Pctlnormrange1= par.normMin,
				Pctlnormrange2= par.normMax,
				Pctlrange1= par.min,
				Pctlrange2= par.max,
				Pctlclampmin= par.clampMin,
				Pctlclampmax= par.clampMax)
		elif ptype in ['float_param', 'float_param_2']:
			_setParValsUnlessExported(p,
				Parnormrange1= par.normMin,
				Parnormrange2= par.normMax,
				Parrange1= par.min,
				Parrange2= par.max,
				Parclampmin= par.clampMin,
				Parclampmax= par.clampMax)
		elif ptype == 'par_drop_menu_2':
			_setParValsUnlessExported(p,
				Pctlmenunames=json.dumps(par.menuNames),
				Pctlmenulabels=json.dumps(par.menuLabels))
		elif ptype == 'menu_param_2':
			_setParValsUnlessExported(p,
				Parmenunames=json.dumps(par.menuNames),
				Parmenulabels=json.dumps(par.menuLabels))
