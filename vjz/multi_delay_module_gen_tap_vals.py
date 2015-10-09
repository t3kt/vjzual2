from numpy import interp

def setupParameters(chop):
	page = chop.appendCustomPage('Custom')
	page.appendInt('Maxtap', label='Max Tap Number')
	page.appendInt('Maxactivetap', label='Max Active Tap')
	page.appendFloat('Range', label='Range', size=2)
	page.appendFloat('Inactiveval', label='Inactive Value')
	page.appendStr('Chan', label='Channel Name')

def cook(chop):
	chop.clear()
	outmin, outmax = chop.par.Range1.eval(), chop.par.Range2.eval()
	maxtap = chop.par.Maxtap.eval()
	maxactive = float(chop.par.Maxactivetap.eval())
	chop.numSamples=maxtap
	vals = []
	inrange=[1.0, float(maxtap)]
	for i in range(1, maxtap+1):
		if i <= maxactive:
			val = interp(float(i), [1.0, maxactive], [outmin, outmax])
		else:
			val = 0
		vals.append(val)
	chop.appendChan(chop.par.Chan).vals=vals