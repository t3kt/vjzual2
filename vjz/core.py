__author__ = 'tekt'

if False:
	import vjz.util as util
else:
	import vjz_util as util

import json

def readState(fname):
	with open(fname, 'r') as f:
		return json.load(f)

def writeState(fname, state):
	with open(fname, 'w') as f:
		json.dump(state, f, indent=2, sort_keys=True)

class VjzSystem:
	def __init__(self, root):
		self.root = root
		self.stateMeta = {}

	def GetModules(self, hidden=False):
		return self.root.findChildren(tags=['vjzmod'], key=lambda m: not m.par.Modhidden or hidden)

	def GetState(self):
		modStates = []
		for m in self.GetModules():
			print('building state for module: %s' % (m.path,))
			modStates.append(m.GetStateDict())
		return {
			'modules': modStates,
			'meta': self.root.fetch('stateMeta', {}),
		}

	def SaveState(self, fname):
		state = self.GetState()
		print('Saving state to %s: %r' % (fname, state))
		writeState(fname, state)

	def SetState(self, state):
		print('Loading state %r' % state)
		for modState in state.get('modules', []):
			if 'path' in modState:
				m = self.root.op(modState['path'])
				if m:
					m.LoadStateDict(modState)
		self.root.store('stateMeta', state.get('meta', {}))

	def LoadState(self, fname):
		print('Loading state from %s' % (fname,))
		state = readState(fname)
		self.SetState(state)
