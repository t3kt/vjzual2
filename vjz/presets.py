__author__ = 'tekt'

print('presets.py initializing')

import json

if False:
	import vjz.util as util
	ParMode = {}
	ParMode.CONSTANT = None
else:
	import vjz_util as util

def _getDataPar(host, i):
	return getattr(host.par, 'Preset%ddata' % i)

def _getPresetName(host, i):
	return getattr(host.par, 'Preset%dname' % i)

class PresetsPanel:
	def __init__(self, comp):
		self.comp = comp

	def AddHostPars(self):
		host = self.comp.par.Hostop.eval()
		page = host.appendCustomPage('Presets')
		for i in range(1,9):
			page.appendStr('Preset%dname' % i, label='Preset %d Name' % i)
			page.appendStr('Preset%ddata' % i, label='Preset %d Data' % i)

	def _GetHostAndPars(self):
		host = self.comp.par.Hostop.eval()
		parpatterns = (self.comp.par.Hostparpattern.eval() or 'Mpar*').split()
		return host, [p for p in host.pars(*parpatterns) if p.mode == ParMode.CONSTANT and not p.isOP]

	def DoesPresetExist(self, i):
		host = self.comp.par.Hostop.eval()
		if not host:
			return False
		data = _getDataPar(host, i)
		if data is None:
			return False
		return data.eval() != ''

	def ClearPreset(self, i):
		host = self.comp.par.Hostop.eval()
		data = _getDataPar(host, i)
		data.val = ''
		name = getattr(host.par, 'Preset%dname' % i)
		name.val = ''

	def LoadPreset(self, i):
		host, hostpars = self._GetHostAndPars()
		# if not host:
		# 	return
		print('loading preset "%s" [%i] in %s' % (_getPresetName(host, i), i, host.path))
		data = _getDataPar(host, i).eval()
		if not data:
			return
		vals = json.loads(data)
		if not vals:
			return
		for (name, val) in vals.items():
			p = getattr(host.par, name, None)
			if p is None:
				print('%s: skipping missing param %s' % (host.path, name))
			else:
				util.setParValue(p, val)

	def SavePreset(self, i):
		host, hostpars = self._GetHostAndPars()
		# if not host:
		# 	return
		print('saving preset "%s" [%i] in %s' % (_getPresetName(host, i), i, host.path))
		vals = {p.name: p.eval() for p in hostpars}
		_getDataPar(host, i).val = json.dumps(vals)

	def ResetHostPars(self):
		host, hostpars = self._GetHostAndPars()
		# if not host:
		# 	return
		print('resetting parameters in %s' % (host.path,))
		for p in hostpars:
			p.val = p.default
