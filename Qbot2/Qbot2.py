#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#	   Qbot2.py
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

# TODO ###########################
#
# LISTING WHAT I HAVE PLANNED: 
# option tags "-f, -x", piping !|, evaluation, chat logging and statistics. 
# Commands that are planned:
# !say !fortune !qfortune !vote !poll !uno !cleverbot !welcome 
# !roll !spin !google !spelz !copy !werewolf !connect4 !holdem !blackjack
#
##################################
u = "ƀ"
import u413lib
import time
CK = '!'
def Command(data, command):
	Command_String = CK+command.lower()
	test_data = data.split()
	if test_data[0].lower() == Command_String:
		if len(test_data) > 1:
			args = test_data[1:]
			args = ' '.join(args)
			return {'Command':True,'Args': args}
		else:
			return {'Command':True,'Args': False}
	else:
		return {'Command':False,'Args': False}
def main():
	client = u413lib.createclient()
	if not client.login('qbot','Qpass'):
		exit()
	chat = client.joinchat('general')
	client.sendRawCommand('channel general')
	while True:
		chatget = chat.get()
		if chatget:
			for text in chatget:
				if text['Type'] == 'Message':
					command = Command(text['Msg'],'say')
					if command['Command']:
						if command['Args']:
							print command['Args']
							chat.send(command['Args'].replace('U413.com','http://www.u413.com'))
		time.sleep(7)
		print 'checking again...'
	return 0

if __name__ == '__main__':
	main()
