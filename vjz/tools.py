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

def setModParamEditModeExprs(params):
	for p in params:
		if not hasattr(p.par, 'Paruimode'):
			print('setModParamEditModeExprs skipping', p)
			continue
		setexpr(p.par.Paruimode, 'ext.vjzmod.par.Modparuimode')
		