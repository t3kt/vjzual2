from numpy import interp

def getTargetPane():
	pane = ui.panes.current
	if pane.type == PaneType.NETWORKEDITOR:
		return pane
	for pane in ui.panes:
		if pane.type == PaneType.NETWORKEDITOR:
			return pane

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
		val = interp(float(i), [0, n-1], [0.0, 1.0])
		selected[i].par.order = val

def setAlignOrderByX():
	setAlignOrderBy('nodeX', False)

def setAlignOrderByY():
	setAlignOrderBy('nodeY', True)

def reloadPython():
	for name in ['vjz_util', 'vjz_params', 'vjz_module', 'vjz']:
		op('/local/modules/' + name).par.reload.pulse(1)

def destroyPars():
	parnames = op('par_names_field/string')[0,0].val.split(' ')
	selected = getSelected()
	print('destroyPars', parnames, selected)
	for o in selected:
		oPars = o.pars(*parnames)
		for p in oPars:
			if p.isCustom:
				p.destroy()

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

_alignDirs = {
	'top': {'attr': 'nodeY', 'calc': max},
    'bottom': {'attr': 'nodeY', 'calc': min},
    'left': {'attr': 'nodeX', 'calc': min},
    'right': {'attr': 'nodeX', 'calc': max},
    'middle': {'attr': 'nodeY', 'calc': _getMiddle},
    'center': {'attr': 'nodeX', 'calc': _getMiddle}
}

def align(dirName):
	selected = getSelected()
	if len(selected) < 2:
		return
	alignment = _alignDirs[dirName]
	attr = alignment['attr']
	calc = alignment['calc']
	vals = [getattr(o, attr) for o in selected]
	newval = calc(vals)
	for o in selected:
		setattr(o, attr, newval)

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

