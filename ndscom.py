#!/usr/bin/python

import socket
import json
import os

class NdsCom():
	def __init__(self, host, port):
		self.address = (host, port)
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def create_item(self, path):
		data = {}
		data['request'] = 'create_item'
		
		if not os.path.isfile(path):
			return 1, ''
		data['path'] = os.path.abspath(path)

		result = self.do_com(data)
		if result['response'] != 0:
			return 1, ''
		else:
			return 0, result['uid']

	def delete_item(self, uid):
		data = {}
		data['request'] = 'delete_item'
		data['uid'] = uid

		result = self.do_com(data)
		if result['response'] != 0:
			return 1
		else:
			return 0

	def get_item(self, uid):
		data = {}
		data['request'] = 'get_item'
		data['uid'] = uid

		result = self.do_com(data)
		if result['response'] != 0:
			return 1, {}
		else:
			return 0, result['item']

	def get_item_count(self):
		data = {}
		data['request'] = 'get_item_count'

		result = self.do_com(data)
		if result['response'] != 0:
			return 1, 0
		return 0, result['item_count']

	def get_uids(self, start, num):
		data = {}
		data['request'] = 'get_uids'
		if start < 0:
			start = 0
		if num < 0:
			retCode, itemCount = self.get_item_count()
			if retCode == 1:
				yield 1, []
			num = itemCount
		
		while num != 0:
			data['start'] = start
			if num > 25:
				data['num'] = 25
			else:
				data['num'] = num

			result = self.do_com(data)
			if result['response'] != 0:
				yield 1, []
			else:
				yield 0, result['uids']
			
			start = start + data['num']
			num = num - data['num']

	def get_path(self, uid):
		data = {}
		data['request'] = 'get_path'
		data['uid'] = uid

		result = self.do_com(data)
		if result['response'] != 0:
			return 1, ''
		return 0, result['path']

	def get_size(self, uid):
		data = {}
		data['request'] = 'get_size'
		data['uid'] = uid

		result = self.do_com(data)
		if result['response'] != 0:
			return 1, 0
		return 0, result['size']

	def get_create_time(self, uid):
		data = {}
		data['request'] = 'get_create_time'
		data['uid'] = uid

		result = self.do_com(data)
		if result['response'] != 0:
			return 1, ''
		return 0, result['create_time']

	def do_com(self, data):
		msg = json.dumps(data)
		self.s.sendto(msg, self.address)
		result,addr = self.s.recvfrom(40960)

		return json.loads(result)
