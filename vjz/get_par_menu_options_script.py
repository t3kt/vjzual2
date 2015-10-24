def setupParameters(dat):
	page = dat.appendCustomPage('Custom')
	page.appendOP('Targetop', label='Operator')
	page.appendStr('Targetpar', label='Parameter')

def cook(dat):
	dat.clear()
	dat.appendRow(['name', 'label'])
	targetOp = dat.par.Targetop.eval()
	targetPar = dat.par.Targetpar.eval()
	if not targetOp or not targetPar:
		return
	p = targetOp.pars(targetPar)[0]
	if not p:
		return
	names = p.menuNames
	labels = p.menuLabels
	for i in range(len(names)):
		dat.appendRow([names[i], labels[i]])
	
