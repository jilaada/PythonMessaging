#!/usr/bin/python
""" cherrypy_example.py

	COMPSYS302 - Software Design
	Author: Jilada Eccleston
	Last Edited: 19/02/2015

	This program uses the CherryPy web server (from www.cherrypy.org).
"""
# Requires:  CherryPy 3.2.2  (www.cherrypy.org)
#            Python  (We use 2.7)
# 


import cherrypy
import urllib
import urllib2
import hashlib
import sys
import json
import sqlite3
from sqlite3 import Error

# =====================
# Database Manipulation
# =====================

# Function that will take a connected database and add the table headers
def createTable():
	sql_create_table_usersRegisters = "CREATE TABLE IF NOT EXISTS userRegister (id INTEGER PRIMARY KEY AUTOINCREMENT, upi TEXT UNIQUE, ip TEXT, public_key TEXT, location INTEGER, last_login TEXT, port TEXT); "
	conn = connectDatabase()
	c = conn.cursor()
	c.execute(sql_create_table_usersRegisters)
	conn.commit()
	conn.close()
	pass

# Function that will take a connected database and add the registered users to the list
def addRegisteredUsers():
	dest = "http://cs302.pythonanywhere.com/listUsers"
	userList = urllib.urlopen(dest)
	list = tuple(userList.read().split(","))
	for user in list:
		addUser(user)
	pass

# Function will add single users one at a time to the database
def addUser(user):
	sql_insert_upi = 'INSERT OR IGNORE INTO userRegister(upi) VALUES(?) '
	conn = connectDatabase()
	c = conn.cursor()
	c.execute(sql_insert_upi, (user,))
	conn.commit()
	conn.close()
	pass

# Refresh Database will refresh and add the the activity of existing users in the list
def refreshDatabase(onlineUsers):
	dict = json.loads(onlineUsers)
	conn = connectDatabase()
	c = conn.cursor()
	for items in dict:
		try:
			sql_update_user = 'UPDATE userRegister SET ip==:ip, location==:location, last_login==:lastLogin, port==:port WHERE upi==:username'
			c.execute(sql_update_user, {"ip":dict[items]['ip'], "location":dict[items]['location'], "lastLogin":dict[items]['lastLogin'], "username":dict[items]['username'], "port":dict[items]['port']})
		except KeyError as e:
			print e
		conn.commit()
	conn.close()
	return dict

def connectDatabase():
	try:
		conn = sqlite3.connect("database.db")
	except Error as e:
		return e
	return conn