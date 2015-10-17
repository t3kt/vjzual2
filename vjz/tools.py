from numpy import interp

setattrs = mod.vjz_util.setattrs
setexpr = mod.vjz_util.setexpr

def getSelected():
	pane = ui.panes.current
	if pane.type == PaneType.NETWORKEDITOR:
		selected= pane.owner.selectedChildren
	else:
		selected = []
	print('tools.getSelected()', selected, 'pane', pane, 'type', pane.type, 'owner', pane.owner)
	return selected

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

def setAlignOrderBy(sortAttrName):
	selected = getSelected()
	n = len(selected)
	selected = sorted(selected, key=lambda o: getattr(o, sortAttrName))
	for i in range(n):
		val = interp(float(i), [0, n-1], [0.0, 1.0])
		selected[i].par.order = val

def setAlignOrderByX():
	setAlignOrderBy('nodeX')

def setAlignOrderByY():
	setAlignOrderBy('nodeY')

def reloadPython():
	for name in ['vjz_util', 'vjz_params', 'vjz_module', 'vjz']:
		op('/local/modules/' + name).par.reload.pulse(1)