#!/usr/bin/python
import commands
import json
from BeautifulSoup import BeautifulSoup
import time
from html2text import html2text

version = "1.5.3"
########################################### LOGIN
# Because this is public the password has
# been removed, to run the bot replace:
# "login user password" with a real 
# username and password and uncomment cmd.

#cmd = """curl -b cookies.txt -c cookies.txt -H 'Content-Type: application/json' -d '{"CommandString": "login user password"}' http://u413.com/Terminal/ExecuteCommand 2> /dev/null"""
output = commands.getoutput(cmd)
output = json.loads(output)
output = output['DisplayArray'][0]['Text']
if "You are already" in output:
	print "Already Logged in..." 
	print "\n\n"
else:
	print output
	print "\n\n"
##########################################
	
## Clear up initial backlogs of chats if any...
cmd = """curl -b cookies.txt -c cookies.txt -H 'Content-Type: application/json' -d '[{"Channel": "QBOT","Minimized": false}]' http://u413.com/Terminal/MainUpdate 2> /dev/null"""
chat_text = commands.getoutput(cmd)

while True:
	try:
		def GetChat(new_chat_text=False):
			'''Get and/or parse chat data, and return formatted data in an array'''
			chatlist = []
			if not new_chat_text: #If data to parse has not been given right to the function. Get it from u413.com.
				cmd = """curl -b cookies.txt -c cookies.txt -H 'Content-Type: application/json' -d '[{"Channel": "QBOT","Minimized": false}]' http://u413.com/Terminal/MainUpdate 2> /dev/null"""
				chat_text = commands.getoutput(cmd)
			else:
				chat_text = new_chat_text
			chat_text = json.loads(chat_text) # Put it all into json format, so we can pull the needed data from it
			try: #If data has been givin to the funtion, use that instead. Right now this is only used for getting what the bot sends and printing it out
				 #but it can be extented to allow parsing any data given to it.
				a = chat_text['ChannelDisplayArray']['QBOT'][0]['Text']
			except KeyError:
				return None #No new chat data is available, return None
			i=0
			try:
				while True:
					soup = BeautifulSoup(chat_text['ChannelDisplayArray']['QBOT'][i]['Text']) #Begin pulling the chats for parsing, one at a time.
					username = soup.contents[1].contents[0] # Get the username from this chat dialog by getting the contents of the html
					timestamp = soup.contents[-1].contents[0] # Get the last option, which is always the timestamp
					x = 1
					link = False #If the first word is a link, used to solve a spacing error.
					message = soup.contents[2][5:] #The first word of the message of the chat
					message = html2text(message) #Convert things like &lt; or &gt; into < or >.
					if message == "\n\n": #If there is no first word, the first word is a link
						link = True
					messageadd = "" # String thats gets appended to message
					while True:
						try:
							if soup.contents[x+2].contents[0] == timestamp: # Keep the loop going adding messages until we reach the timestamp
								break
							messageadd = soup.contents[x+2].contents[0]
							if link:
								messageadd = messageadd+" "
								link = False
							else:
								messageadd = " "+messageadd+" "
						except:
							messageadd = html2text(soup.contents[x+2])
						message += messageadd
						x += 1
					message = message.replace("\n\n","") #Eliminate newlines so that the text shows up in terminal correctly
					chatlist.append([username,message,timestamp]) #Add to the list, [[username,message,timestamp], [username,message,timestamp]] format
					i += 1 #iterate to the next dialog
			except IndexError: #When we reach the last chat the we received, send the chat array
				return chatlist
				
				
				
				
				
				
				
		#####################################
		#
		# Start Actual bot code
		#
		#####################################
		CK = "!" #Command key, used before commands to detonate them.
		##################################################
		# Start bot function area.
		#
		# Here you can create extensions to use in the
		# command code area. You can also put whole 
		# commands here if they are exceedingly complex.
		##################################################
		def Command(data, command):
			'''Test for a command, return if command is there and arguments'''
			
			#Make everythin lowercase except Args
			data2 = data.lower() 
			command = command.lower()
			Command_String = CK+command
			Test_String = data2[:(len(command)+len(CK))]
			Args = data[(len(command)+len(CK)+1):]
			if Args == "": #If there are no arguments
				if Command_String == Test_String:
					return [True,None]
				else:
					return [False]
			else:
				if Command_String+" " == data2[:(len(command)+len(CK)+1)]:
					return [True,Args]
				else:
					return [False]
		def Send(data): 
			'''Send text to chat'''
			###################################################
			# Below I create a file with my command then use
			# the file with curl to send data to chat, they
			# allows me to send strings with characters such
			# as a single quote.
			####################################################
			filename = "senq.txt"
			file = open(filename, 'w') # Overwrite the file everythime
			file.write("""{"CommandString": "channel QBOT """+data+""""}\n""")
			file.close
			# For some reason the file has to be opened and closed again for this to work
			file = open(filename, 'r')
			file.close
			cmd = """curl -b cookies.txt -c cookies.txt -H 'Content-Type: application/json' -d @senq.txt http://u413.com/Terminal/ExecuteCommand 2> /dev/null"""
			mystring = commands.getoutput(cmd)
			mychat = GetChat(mystring) #Send data to GetChat() to parse, mychat = the array.
			if mychat is not None: #Use same method as below to add data to terminal
				for data in mychat:
					u = data[0] #User
					m = data[1] #Message
					t = data[2] #TimeStamp
					# Print out data to terminal, with colors
					print "\033[2m" + "<" + "\033[0m"+"\033[1m" + "\033[40m" + data[0] + "\033[0m"+"\033[2m" + ">" + "\033[0m","\033[40m" +  data[1] + "\033[0m","\033[1;30m" + data[2] + "\033[0m"
		##################################################
		# End bot function area.
		##################################################
		while True:
			Chat = GetChat() #Get new chat data.
			if Chat is not None: #If new chat data exists
				for data in Chat:
					u = data[0] #User
					m = data[1] #Message
					t = data[2] #TimeStamp
					# Print out data to terminal, with colors
					print "\033[2m" + "<" + "\033[0m"+"\033[1m" + "\033[40m" + data[0] + "\033[0m"+"\033[2m" + ">" + "\033[0m","\033[40m" +  data[1] + "\033[0m","\033[1;30m" + data[2] + "\033[0m"
					###################################################
					# Begin actual bot command code
					#
					# All chat commands should be placed here.
					#
					# Any complexities should be placed in the bot
					# function area. All commands should be simple,
					# short and most of their work should be done
					# by calling functions in the bot function area.
					# 
					# This is so a person can create their own 
					# functions without having to understand the 
					# whole bot. They should be able to easily 
					# manipulate exsisting functions to make their 
					# own. And it should be mostly as easy as 
					#            Test--->Action--->Send
					# without them having to understand what those do.
					###################################################
					
					if Command(m, "say")[0]: #If the user send this command
						args = Command(m, "say")[1]
						if args: #If there are any arguments
							Send(args) # Send argumens to chat.
					if Command(m, "cowsay")[0]:
						args = Command(m, "cowsay")[1]
						if args:
							cow_pic = """\\n ._______(o o) - """ + args + """\\n (_u413_\\/.(__) \\n .||....|| """
							Send(cow_pic)
					############################################
					# End actual bot command code
					############################################
			time.sleep(7) #Try to get new chat every 7 seconds.
		#####################################
		#
		# End Actual bot code
		#
		#####################################
			
	except:
		continue
