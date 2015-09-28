from vjz_params import VjzParam
import vjz_util as util

class MenuParam(VjzParam):
	def __init__(self, comp):
		VjzParam.__init__(self, comp)

	def Initialize(self):
		VjzParam.Initialize(self)
		page = self.GetParamPage()
		util.setattrs(page.appendInt('Parlistsize', label='List Items')[0],
					  min=1,
					  normMin=1,
					  clampMin=1,
					  normMax=10,
					  default=5)