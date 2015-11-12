__author__ = 'tekt'

from numpy import interp

import time
import os

print('util.py initializing')

_dbglog = None

def _DBGLOG_full(msg):
	# global _dbglog
	# if _dbglog is None:
	# 	_dbglog = open('DEBUGLOG.txt', 'w')
	# 	_dbglog.write('----BEGIN DEBUG LOG [%r]----\n' % time.time())
	formatted = '%r\t%s\n' % (time.time(), msg)
	_dbglog.write(formatted)
	print(formatted)
	_dbglog.flush()

def _DBGLOG_basic(msg):
	formatted = '%r\t%s\n' % (time.time(), msg)
	print(formatted)

if os.environ['VJZDEBUG'] == '1':
	_dbglog = open('DEBUGLOG.txt', 'w')
	_dbglog.write('----BEGIN DEBUG LOG [%r]----\n' % time.time())
	DBGLOG = _DBGLOG_full
else:
	DBGLOG = _DBGLOG_basic

def dumpObject(obj, underscores=False, methods=False):
	print('Dump ' + repr(obj) + ' type:' + repr(type(obj)))
	for key in dir(obj):
		if key.startswith('_') and not underscores:
			continue
		val = getattr(obj, key)
		if callable(val) and not methods:
			continue
		print('  ' + key + ': ' + repr(val))

def dumpMethodHelps(obj, underscores=False):
	print('Methods of ' + repr(obj) + ' type:' + repr(type(obj)))
	for key in dir(obj):
		if key.startswith('_') and not underscores:
			continue
		val = getattr(obj, key)
		if callable(val):
			print(help(getattr(obj, key)))

def argToOp(arg):
	if not arg:
		return None
	if isinstance(arg, str):
		o = op(arg)
		if not o:
			raise Exception('operator not found: ' + arg)
		return o
	return arg

def argToPath(arg):
	if not arg:
		return ''
	if isinstance(arg, str):
		return arg
	if hasattr(arg, 'path'):
		return arg.path
	return arg

def setattrs(obj, **attrs):
	if isinstance(obj, (tuple,list)):
		for o in obj:
			setattrs(o, **attrs)
	else:
		for key in attrs:
			setattr(obj, key, attrs[key])

def setexpr(par, expr):
	if isinstance(par, (tuple, list)):
		for p in par:
			setexpr(p, expr)
	else:
		par.mode = ParMode.EXPRESSION
		par.expr = expr

def setParExprs(obj, **exprs):
	if isinstance(obj, (tuple, list)):
		for o in obj:
			setParExprs(o, **exprs)
	else:
		for key in exprs:
			setexpr(getattr(obj.par, key), exprs[key])

def setParValues(obj, **values):
	if isinstance(obj, (tuple, list)):
		for o in obj:
			setParValues(o, **values)
	else:
		for key in values:
			setParValue(getattr(obj.par, key), values[key])

def coerceBool(val):
	return val is True or val == 1 or val == '1' or val == 'True'

def setParValue(par, val):
	if val == '':
		return
	if par.isToggle:
		par.val = coerceBool(val)
	elif par.isFloat:
		par.val = float(val)
	elif par.isInt:
		par.val = int(val)
	elif par.isMenu:
		if isinstance(val, (int, float)):
			par.menuIndex = int(val)
		else:
			par.val = val
	# elif par.isString:
	else:
		par.val = val
	par.mode = ParMode.CONSTANT

def setPars(op, **parValues):
	if isinstance(op, (tuple, list)):
		for o in op:
			setPars(o, **parValues)
	else:
		for name in parValues:
			setParValue(getattr(op.par, name), parValues[name])

def evalPars(pars):
	return [p.eval() for p in pars]

def interpLists(ratio, start, end):
	result = []
	inrange = [0, 1]
	for i in range(len(start)):
		result.append(
			interp(ratio,
			       inrange,
			       [start[i], end[i]]))
	return result

def clamp(val, low, high):
	return max(low, min(val, high))

def overrideRows(tbl, **overrides):
	tbl = argToOp(tbl)
	if not tbl:
		return
	for key in overrides:
		tbl[key, 1] = overrides[key]

def updateTableRow(tbl, rowKey, vals, addMissing=False, ignoreMissingCols=False):
	tbl = argToOp(tbl)
	if not tbl:
		return
	if not tbl[rowKey, 0]:
		if not addMissing:
			raise Exception('row ' + rowKey + ' not found in table ' + tbl)
		else:
			tbl.appendRow([rowKey])
	for colKey in vals:
		v = vals[colKey]
		if ignoreMissingCols and tbl[rowKey, colKey] is None:
			continue
		tbl[rowKey, colKey] = v if v is not None else ''

def fillParamsTable(tbl, pars, find=None, replace=None):
	tbl = argToOp(tbl)
	tbl.clear()
	for p in pars:
		name = p.name
		if find:
			name = name.replace(find, replace)
		tbl.appendRow([name, p.eval()])

def fillParamsExportTable(exports, pars, sourcePath="", targetPath="", find=None, replace=None):
	exports = argToOp(exports)
	exports.clear()
	exports.appendRow(['path', 'parameter', 'value'])
	for p in pars:
		name = p.name
		if find:
			name = name.replace(find, replace)
		exports.appendRow([targetPath, name, "`par('" + sourcePath + "/" + p.name + "')`"])

def fillParamMenuOptionsTable(tbl, p):
	tbl = argToOp(tbl)
	tbl.clear()
	for i in range(len(p.menuNames)):
		tbl.appendRow([p.menuNames[i], p.menuLabels[i]])

def ApplyPythonProxyExprs(targetComp, exprPrefix, **mappings):
	cpar = targetComp.par
	for destName in mappings.keys():
		setexpr(getattr(cpar, destName),
		        exprPrefix + mappings[destName])

def GetParamDict(op, *paramNames):
	return {pname: getattr(op.par, pname).eval() for pname in paramNames}

def GetClonedAncestor(op):
	while op:
		if hasattr(op.par, 'clone') and op.par.clone.eval():
			return op
		op = op.parent()
	return None
