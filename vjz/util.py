__author__ = 'tekt'

print('util.py initializing')

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

def coerceBool(val):
	return val is True or val == 1 or val == '1' or val == 'True'

def setParValue(par, val):
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
	for name in parValues:
		setParValue(getattr(op.par, name), parValues[name])

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