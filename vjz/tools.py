from numpy import interp

setattrs = mod.vjz_util.setattrs
setexpr = mod.vjz_util.setexpr

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
	print('tools.getSelected()', selected, 'pane', pane, 'type', pane.type, 'owner', pane.owner)
	return selected

def logSelected():
	getSelected() # it already has a print statement

def initSelected():
	selected = getSelected()
	for o in selected:
		init = o.op('init')
		if init:
			init.run()

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
		setexpr(p.par.Paruimode, 'ext.vjzmod.par.Modparuimode')

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
	selected = sorted(selected, key=lambda o: getattr(o, sortAttrName))
	if reverseDir:
		selected = list(reversed(selected))
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
	if not comp.isCOMP:
		return False
	toxfile = comp.par.externaltox.eval()
	if not toxfile:
		return False
	comp.save(toxfile)
	ui.status = 'Saved TOX %s to %s' % (comp.path, toxfile)
	return True

def saveSelectedTox():
	selected = getSelected()
	for comp in selected:
		_saveTox(comp)

def saveActiveTox():
	pane = getTargetPane()
	comp = pane.owner
	while comp:
		if _saveTox(comp):
			return
		comp = comp.parent()

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

