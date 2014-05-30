#!/usr/bin/python

import hashlib
import os
from datetime import *
import time

def get_uid(path):
	return getMd5(path)

def get_md5(path):
	m = hashlib.md5()
	fileHandle = open(path, 'rb')
	m.update(fileHandle.read())
	value = m.hexdigest()
	fileHandle.close()

	return value

def get_size(path):
	return os.path.getsize(path)

def set_timezone():
	os.environ['TZ'] = 'Asia/Shanghai'
	time.tzset()

def get_current_time():
	curTime = datetime.now()
	return curTime.strftime('%Y-%m-%d %H:%M:%S')

def get_abstract_path(path):
	if os.path.isabs(path):
		return path
	return os.path.abspath(path)

def enable_dir(path):
	if not os.path.exists(path):
		os.makedirs(path)
