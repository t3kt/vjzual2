__author__ = 'tekt'


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
	for key in attrs:
		setattr(obj, key, attrs[key])

def setexpr(p, expr):
	p.mode = ParMode.EXPRESSION
	p.expr = expr

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