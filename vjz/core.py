__author__ = 'tekt'

from vjz import util

def _getExt(comp, clazz, testattr):
	comp = util.argToOp(comp)
	if hasattr(comp, testattr):
		return comp
	if comp.ext and hasattr(comp.ext, clazz.__name__):
		return getattr(comp.ext, clazz.__name__)
	if comp.extensions:
		for e in comp.extensions:
			if isinstance(e, clazz):
				return e
	print('unable to find ' + clazz.__name__ + ' extension for comp: ' + comp.path)

class VjzParam:
	@staticmethod
	def fromOp(op):
		return _getExt(op, VjzParam, 'pVar')

	def __init__(self, comp):
		self._comp = comp
		self.pDef = comp.op(comp.var('pdef'))

	def pDefProp(self, name, defaultVal=None):
		cell = self.pDef[name, 1]
		return cell.val if cell else defaultVal

	def pVar(self, name):
		return self._comp.var(name)

	@property
	def paramPath(self):
		return self._comp.path

class VjzModule:
	@staticmethod
	def fromOp(op):
		return _getExt(op, VjzParam, 'modVar')

	def __init__(self, comp):
		self._comp = comp

	def modVar(self, name):
		return self._comp.var(name)

	@property
	def modName(self):
		return self.modVar('modname')

class VjzSystem:
	def __init__(self, root):
		self.root = root