setattrs = mod.vjz_util.setattrs
setexpr = mod.vjz_util.setexpr

class ColorParams:
	def __init__(self, comp):
		self._comp = comp

	def Initialize(self):
		page = self._comp.appendCustomPage('Color Par Sliders')
		page.appendOP('Pcolop', label='Target Operator')
		page.appendStr('Pcolrpar', label='Red Parameter')
		page.appendStr('Pcolgpar', label='Green Parameter')
		page.appendStr('Pcolbpar', label='Blue Parameter')
		page.appendStr('Pcolhpar', label='Hue Parameter')
		page.appendStr('Pcolspar', label='Saturation Parameter')
		page.appendStr('Pcolvpar', label='Value Parameter')
		setattrs(page.appendMenu('Pcoleditmode', label='Color Edit Mode')[0],
		         menuNames=['rgb', 'hsv'],
		         menuLabels=['RGB', 'HSV'])
		setattrs(page.appendMenu('Pcoldatamode', label='Color Data Mode')[0],
		         menuNames=['rgb', 'hsv'],
		         menuLabels=['RGB', 'HSV'])
		self.UpdateModeParamStates()

	def UpdateModeParamStates(self):
		c = self._comp
		editMode = c.par.Pcoleditmode.eval()
		dataMode = c.par.Pcoldatamode.eval()
		if dataMode == 'rgb':
			rgbEnabled = True
			hsvEnabled = False
			rgbTargetOp = 'me.parent().par.Pcolop'
			hsvTargetOp = 'op("hsv_to_rgb")'
			rgbPars = ['me.parent().par.Pcolrpar',
			           'me.parent().par.Pcolgpar',
			           'me.parent().par.Pcolbpar']
			hsvPars = ['"H"', '"S"', '"V"']
			updateHsvFromRgbEnabled = False
			updateRgbFromHsvEnabled = editMode == 'hsv'
		#elif dataMode == 'hsv':
		else:
			rgbEnabled = False
			hsvEnabled = True
			rgbTargetOp = 'op("rgb_to_hsv")'
			hsvTargetOp = 'me.parent().par.Pcolop'
			rgbPars = ['"R"', '"G"', '"B"']
			hsvPars = ['me.parent().par.Pcolhpar',
			           'me.parent().par.Pcolspar',
			           'me.parent().par.Pcolvpar']
			updateHsvFromRgbEnabled = editMode == 'rgb'
			updateRgbFromHsvEnabled = False

		c.par.Pcolrpar.enable = rgbEnabled
		c.par.Pcolgpar.enable = rgbEnabled
		c.par.Pcolbpar.enable = rgbEnabled

		c.par.Pcolhpar.enable = hsvEnabled
		c.par.Pcolspar.enable = hsvEnabled
		c.par.Pcolvpar.enable = hsvEnabled

		setexpr([c.op('r_param').par.Parop,
		         c.op('g_param').par.Parop,
		         c.op('b_param').par.Parop],
		        rgbTargetOp)

		setexpr([c.op('h_param').par.Parop,
		         c.op('s_param').par.Parop,
		         c.op('v_param').par.Parop],
		        hsvTargetOp)

		setexpr(c.op('r_param').par.Parpar, rgbPars[0])
		setexpr(c.op('g_param').par.Parpar, rgbPars[1])
		setexpr(c.op('b_param').par.Parpar, rgbPars[2])

		setexpr(c.op('h_param').par.Parpar, hsvPars[0])
		setexpr(c.op('s_param').par.Parpar, hsvPars[1])
		setexpr(c.op('v_param').par.Parpar, hsvPars[2])

		c.op('update_hsv_from_rgb').par.active = updateHsvFromRgbEnabled
		c.op('update_rgb_from_hsv').par.active = updateRgbFromHsvEnabled

