import vjz_util as util

class ClipTimeSource:
	def __init__(self, comp):
		self._comp = comp

	def Initialize(self):
		page = self._comp.appendCustomPage('ClipTimeSource')
		util.setattrs(page.appendFloat('Timectlmaxrate', label='Maximum Rate setting')[0],
		              min=0, clampMin=True, normMax=5, default=2)
		util.setattrs(page.appendFloat('Timectlrate', label='Rate')[0],
		              min=0, clampMin=True, normMax=5, default=1)
		util.setattrs(page.appendMenu('Timectlloopmode', label='Loop Mode')[0],
		              menuNames=['loop', 'zigzag'], menuLabels=['Loop', 'Zig-Zag'])
		util.setattrs(page.appendMenu('Timectlstate', label='Playback State')[0],
		              menuNames=['forward', 'backward', 'paused'],
		              menuLabels=['Forward', 'Backward', 'Paused'])
		util.overrideRows(self._comp.op('rateslider/define'),
		                  label="rate", channelname="rate",
		                  upper_range="`par($vjztimectl + '/Timectlmaxrate')`")

	def Reverse(self):
		state = self._comp.par.Timectlstate
		if state == 'forward':
			state.val = 'backward'
		elif state == 'backward':
			state.val = 'forward'
		# if 'paused' don't do anything

	def HandleTimerCycleEnd(self):
		if self._comp.par.Timectlloopmode == 'zigzag':
			self.Reverse()
