from vjz_params import VjzParam
import vjz_util as util

class BoolParam(VjzParam):
	def __init__(self, comp):
		VjzParam.__init__(self, comp)

	def Initialize(self):
		VjzParam.Initialize(self)
		page = self.GetParamPage()
		page.appendStr('Parofftext', label='Button Off Text')
		page.appendStr('Paroffhelptext', label='Button Off Help Text')
