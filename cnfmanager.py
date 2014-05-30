#!/usr/bin/python

import ConfigParser
import os

class CnfManager():
	def load(self, cnfFile):
		if not os.path.isfile(cnfFile):
			cnfFile = './ndss.cnf'

		cf = ConfigParser.ConfigParser()
		cf.read(cnfFile)

		self.cnfData = {}
		self.cnfData['comPort'] = int(cf.get('com', 'comPort'))

	def get_cnf_data(self):
		return self.cnfData
