__author__ = 'tekt'

if False:
	import vjz.util as util
else:
	import vjz_util as util

import json

class VjzSystem:
	def __init__(self, root):
		self.root = root

	def GetModules(self, hidden=False):
		return self.root.findChildren(tags=['vjzmod'], key=lambda m: not m.par.Modhidden or hidden)

	def GetState(self):
		modStates = []
		for m in self.GetModules():
			print('building state for module: %s' % (m.path,))
			modStates.append(m.GetStateDict())
		return {
			"modules": modStates
		}

	def SaveState(self, fname):
		state = self.GetState()
		print('Saving state to %s: %r' % (fname, state))
		with open(fname, 'w') as f:
			json.dump(state, f, indent=2)

	def SetState(self, state):
		print('Loading state %r' % state)
		for modState in state.get('modules', []):
			if 'path' in modState:
				m = self.root.op(modState['path'])
				if m:
					m.LoadStateDict(modState)

	def LoadState(self, fname):
		print('Loading state from %s' % (fname,))
		with open(fname, 'r') as f:
			state = json.load(f)
		self.SetState(state)
