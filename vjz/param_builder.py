import collections

if False:
	import vjz.util as util
else:
	import vjz_util as util

setattrs = util.setattrs

_paramSettingNames = [
	'default', 'enable', 'order',
	'min', 'max', 'normMin', 'normMax', 'clampMin', 'clampMax',
	'menuNames', 'menuLabels'
]
ParamSpec = collections.namedtuple(
	'ParamSpec',
	_paramSettingNames + [
		'name', 'label', 'style',
	])

def _getCellVal(cell, default=None, parse=None):
	if not cell or not cell.val:
		return default
	if parse:
		val = parse(cell.val)
		return val if val is not None else default
	return cell.val

def _getCellInt(cell, default=None):
	return _getCellVal(cell, default=default, parse=int)

def _getCellFloat(cell, default=None):
	return _getCellVal(cell, default=default, parse=float)

def _getCellBool(cell, default=None):
	return _getCellVal(cell, default=default, parse=util.coerceBool)

def _prepArgs(spec, **kwargs):
	result = {}
	for key in kwargs:
		val = getattr(spec, key, default=kwargs[key])
		if val is not None:
			result[key] = val
	return result


def _getSpecPage(obj, spec):
	if spec.page:
		return obj.appendCustomPage(spec.page)
	if obj.customPages:
		return obj.customPages[0]
	return obj.appendCustomPage('Custom')


class ParamStyle:
	def __init__(self, create=None, args=None):
		self._createMethod = create
		if args:
			self._createArgs = dict(args)
		else:
			self._createArgs = {'label': None, 'order': None, 'replace': True}

	def createParam(self, obj, spec):
		page = _getSpecPage(obj, spec)
		parTuple = self._create(obj, page, spec)
		for par in parTuple:
			for name in _paramSettingNames:
				val = getattr(spec, name)
				if val is not None:
					setattr(par, name, val)

	def _create(self, obj, page, spec):
		if not self._createMethod:
			raise NotImplementedError('_create not implemented')
		args = _prepArgs(spec, **self._createArgs)
		return getattr(page, self._createMethod)(page, **args)

	def readRowSpec(self, dat, row):
		return ParamSpec(
			name=_getCellVal(dat[row, 'name']),
		    label=_getCellVal(dat[row, 'label']),
		    order=_getCellVal(dat[row, 'order']),
		    replace=_getCellBool(dat[row, 'replace']),
		    enable=_getCellBool(dat[row, 'enable']),
			default= _getCellVal(dat[row, 'default']),
		    min=_getCellFloat(dat[row, 'min']),
		    max=_getCellFloat(dat[row, 'max']),
		    normMin=_getCellFloat(dat[row, 'normMin']),
		    normMax=_getCellFloat(dat[row, 'normMax']),
		    clampMin=_getCellBool(dat[row, 'clampMin']),
		    clampMax=_getCellBool(dat[row, 'clampMax']),
		    # size=_getCellInt(dat[row, 'size']),
		)


class SizedNumberGroupStyle(ParamStyle):
	def __init__(self, create=None, args=None):
		ParamStyle.__init__(self, create=create, args=args)
		self._createArgs.setdefault('size', 1)

	def readRowSpec(self, dat, row):
		spec = ParamStyle.readRowSpec(self, dat, row)
		spec.size = _getCellInt(dat[row, 'size'])
		return spec


class NumberGroupStyle(ParamStyle):
	def __init__(self, create=None, args=None):
		ParamStyle.__init__(self, create=create, args=args)


styles = {}

for style in ['Str', 'StrMenu', 'Toggle', 'Pulse', 'Menu',
              'OBJ', 'PanelCOMP', 'COMP', 'SOP', 'MAT', 'CHOP', 'TOP', 'DAT', 'OP',
              'File', 'Folder']:
	styles[style.lower()] = ParamStyle('append' + style)

for style in ['RGB', 'RGBA', 'UV', 'UVW', 'WH', 'XY', 'XYZ']:
	styles[style.lower()] = NumberGroupStyle('append' + style)

for style in ['Float', 'Int']:
	styles[style.lower()] = SizedNumberGroupStyle('append' + style)

def readRowSpec(dat, row):
	styleName = _getCellVal(dat[row, 'style'])
	handler = styles[styleName]
	if not handler:
		raise Exception('Unsupported style: ' + styleName)
	return handler.readRowSpec(dat, row)

def readRowSpecs(dat):
	return [readRowSpec(dat, row) for row in range(1, dat.numRows)]

