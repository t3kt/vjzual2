def getColumnNames(dat):
	return ['name', 'mapctrl', 'device', 'ctrl']

def getRowValues(dat, param, row):
	if not param.par.Parmapenabled.eval():
		return ['', '', '', '']
	mapctrl = param.par.Parmapctrl.eval()
	if not mapctrl or mapctrl in ['--', 'none']:
		return ['', '', '', '']
	parts = mapctrl.split(':')
	if len(parts) != 2:
		return ['', '', '', '']
	device, ctrl =  parts
	return [param.par.Parid.eval(), mapctrl, device, ctrl]

def includeRow(dat, curOp, row):
	mapping = curOp.op('midi_mapping')
	if not mapping or not curOp.par.Parmapenabled.eval() or curOp.par.Parmapctrl.eval() in ['--', 'none']:
		return False
	return True
	