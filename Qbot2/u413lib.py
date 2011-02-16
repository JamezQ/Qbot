#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#	   u413lib.py
#	   
#	   Copyright 2011 James McClain <jamezmcclain@gmail.com>
#	   
#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU General Public License as published by
#	   the Free Software Foundation; either version 3 of the License, or
#	   (at your option) any later version.
#	   
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU General Public License for more details.
#	   
#	   You should have received a copy of the GNU General Public License
#	   along with this program; if not, write to the Free Software
#	   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#	   MA 02110-1301, USA.

# TODO #######################
#
# Emotes in chat return extra spaces, fix that
# Fix htmlentities
# 
# Make a __action__ method, adding channels, users, or so on.
# Make client.login() automatically append client.channels if True
# Make client.joinchat() append to client.chatters[]
# Make a log() method to write all chat to a file
#
# client.joinchat() gets userlist in that chat.
# Crases on /users and /help
#
# Make joinchat join a chat if client.channels does contain the joinchat
# channel.
###############################
import urllib2
import json
from BeautifulSoup import BeautifulSoup
class createclient(object):
	"""create a client, with a cookiejar"""
	def __init__(self):
		self.o = urllib2.build_opener( urllib2.HTTPCookieProcessor() )
		urllib2.install_opener( self.o )
	def login(self,username,password):
		"""Attempt to login, return True if succesful, False otherwise"""
		data = self.sendRawCommand('login '+username+' '+password)
		data = json.loads(data)
		data = data['DisplayArray'][0]['Text']
		if "You are already" in data:
			return True
		elif "You are now" in data:
			return True
		else:
			return False
	def sendRawCommand(self,command):
		"""Send a raw command and get raw json back"""
		req = urllib2.Request("http://u413.com/Terminal/ExecuteCommand",
		headers = {
		"Content-Type": "application/json",
		"Accept": "*/*",   
		"User-Agent": "my-python-app/1", 
		},
		data = '''{"CommandString":"'''+command+'''"}''')
		a = self.o.open(req)
		return a.read()
	def getRawChat(self,channel):
		"""Get raw json back from a chat update"""
		channel = channel.upper()
		req = urllib2.Request("http://u413.com/Terminal/MainUpdate",
		headers = {
		"Content-Type": "application/json",
		"Accept": "*/*",   
		"User-Agent": "my-python-app/1", 
		},
		data = '''[{"Channel": "'''+channel+'''","Minimized": false}]''')
		a = self.o.open(req)
		return a.read()
	def joinchat(self,channel):
		"""Create a chatter object"""
		channel = channel.upper()
		return self.__joinchat__(channel,self)
	class __joinchat__(object):
		def __init__(self,channel,me):
			self.channel = channel
			self.me = me
		def get(self):
			"""Return parsed updated chat, if no updates, return false"""
			chat = parse_chat(self.me.getRawChat(self.channel))
			if chat:
				return chat[self.channel]
			else:
				return False
		def send(self,chatstring):
			"""Send string to chat chatter in in"""
			cmd = "channel "
			cmd += self.channel
			cmd += ' '
			cmd += chatstring
			cmd = cmd.encode('utf8')
			chat = self.me.sendRawCommand(h2t(cmd))
			chat = parse_chat(chat)
			if chat:
				return chat[self.channel]
			else:
				return False
			
			
def parse_chat(parsedata):
	"""Parse chat data, put in dictionary"""
	parsedata = json.loads(parsedata)
	parsed_chat_data = {}
	for channel in parsedata['ChannelDisplayArray']:
		messagelist = []
		for Text in parsedata['ChannelDisplayArray'][channel]:
			messagelist.append(Text['Text'])
		for message in range(len(messagelist)):
			messagelist[message] = BeautifulSoup(messagelist[message])
		i = 0
		for message in messagelist:
			message_dict = {}
			
			# Get Message Type
			if message.contents[0] == "-= ":
				message_dict['Type'] = u"Announcement"
			elif message.contents[0] == "&lt;":
				message_dict['Type'] = u"Message"
			else:
				message_dict['Type'] = u"Emote"
				
			# Get username
			if message_dict['Type'] is u"Message":
				message_dict['User'] = message.contents[1].contents[0]
			elif message_dict['Type'] is u"Emote":
				message_dict['User'] = message.contents[0].contents[1].\
				contents[0]
			elif message_dict['Type'] is u"Announcement":
				message_dict['User'] = message.contents[1].contents[0]
			
			# Get Message
			message_dict['Msg'] = ''
			if message_dict['Type'] is u"Message":
				for text in message.contents[2:-1]:
					try:
						message_dict['Msg'] += text.contents[0]
					except AttributeError:
						message_dict['Msg'] += text
					except IndexError:
						if str(text) == "<br />":
							message_dict['Msg'] += '\n'
						else:
							raise
				message_dict['Msg'] = message_dict['Msg'][5:-1]
				if message_dict['Msg'][-1] == " ":
					message_dict['Msg'] = message_dict['Msg'][:-1]
				
			elif message_dict['Type'] is u"Emote":
				for text in message.contents[1:-1]:
					try:
						message_dict['Msg'] += text.contents[0]
					except AttributeError:
						message_dict['Msg'] += text
					except IndexError:
						if str(text) == "<br />":
							message_dict['Msg'] += '\n'
						else:
							raise
				if message_dict['Msg'][-1] == " ":
					message_dict['Msg'] = message_dict['Msg'][:-1]
			elif message_dict['Type'] is u"Announcement":
				message_dict['Msg'] += message.contents[2][1:-4]
			message_dict['Msg'] = message_dict['Msg']
			#Get Timestamps
			message_dict['Timestamp'] = message.contents[-1].contents[0]
			
			
			messagelist[i] = message_dict
			i += 1
		parsed_chat_data[channel] = messagelist
	return parsed_chat_data

def h2t(text):
	"""Convert Html to Text"""
	text = text.replace('&lt;','<')
	text = text.replace('&gt;','>')
	text = text.replace('&#39;',"'")
	text = text.replace('\\',"\\\\")
	text = text.replace('&quot;','''\\"''')
	text = text.replace('&amp;','&')
	return text
