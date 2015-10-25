util = mod.vjz_util

def setupParameters(dat):
	page = dat.appendCustomPage('Custom')
	page.appendCOMP('Modop', label='Module')
	page.appendStr('Parnames', label='Parameters')
	page.appendToggle('Setfontsize', label='Set Font Size')
	util.setattrs(page.appendInt('Fontsize', label='Font Size')[0],
				  default=12, min=1, normMin=1, normMax=30, clampMin=True)


def cook(dat):
	dat.clear()
	dat.appendRow(['path', 'parameter', 'value'])
	dat.appendRow(['*_param', 'Parop', 'ext.vjzmod'])
	#dat.appendRow(['*_param', 'Paruimode', 'ext.vjzmod.par.Modparuimode'])
	if dat.par.Setfontsize.eval():
		dat.appendRow(['*_param', 'Parfontsize', dat.par.Fontsize.eval()])
	m = dat.par.Modop.eval()
	if not m:
		return
	names = dat.par.Parnames.eval()
	if names:
		names = names.split()
	else:
		names = ['Mpar*']
	mpars = m.pars(*names)
	for p in mpars:
		name = p.name.replace('Mpar', '')
		paramOp = name + '_param'
		dat.appendRow([paramOp, 'Parpar', repr(p.name)])
		dat.appendRow([paramOp, 'Parlocalname', repr(name)])
		dat.appendRow([paramOp, 'Parlabel', repr(name)])
