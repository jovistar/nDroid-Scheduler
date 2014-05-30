#!/usr/bin/python

import json

class MsgManager():
	def res_request(self, msg):
		data = json.loads(msg)
		cmds = ['scan', 'report', 'create_item', 'update_state']

		if data['request'] == None:
			return 1, {}

		if data['request'] not in cmds:
			return 1, {}

		return 0, data

	def gen_response(self, data):
		return json.dumps(data)
