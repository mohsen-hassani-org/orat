#!/usr/bin/python3
import socket 
import time

import aditional_functions as ad
import global_variables as gv

# =====================================================================
# BROADCAST HANDLER
# =====================================================================


def bc_help_menu():
	print('')
	print("Broadcast status\t - Set delays beetwen sending broadcast messages (Sec)")
	print('========================================================================')
	print('Variable\t\tVlaue\t\tDescription')
	print('------------------------------------------------------------------------')
	print('bc_flag\t\t\t%s\t\tSet True to send broadcast messages. False to disable it' % gv.SENDING_BROADCAST)
	print('bc_delay\t\t%s\t\tDelay beetwen sending broadcast messages (Sec)' % gv.BROADCAST_DELAY)
	print('bc_ip\t\t\t%s\tIP Address to send as broadcast' % gv.BROADCAST_IP_TO_SEND)
	print('bc_notifications\t%s\t\tShow notifications about sending broadcast' % gv.BROADCAST_NOTIFICATION)
	print('')
	print('')
	print("set_flag \t - Stop or Start sending broadcast messages on the network")
	print("set_delay \t - Set delay beetwen sending broadcast messages (Sec)")
	print("set_ip \t\t - IP to send broadcast on network")
	print("set_notifs \t - Enable or disable broadcast notifications")
	print('')


def interactive_bc_menu():
	input_variable = input('\tChoose Variable(Enter to return)>')	
	if(str(bytes(input_variable, 'utf-8')) == "b''"): 
		print('returning')
		return
	variable = str(input_variable)
	if(variable == 'set_flag'):
		input_value = input('\t\tChoose Value(T or F)>')	
		if(str(bytes(input_value, 'utf-8')) == "b''"): 
			print('returning')
			return
		value = str(input_value)
		if(value == 'T'):
			gv.SENDING_BROADCAST = True
		elif(value == 'F'):
			gv.SENDING_BROADCAST = False
		else:
			print('Wrong answer. returning...')
			return
	elif(variable == 'set_delay'):
		input_value = input('\t\tChoose Value(sec)>')	
		if(str(bytes(input_value, 'utf-8')) == "b''"): 
			print('returning')
			return
		try:
			value = int(input_value)
		except:
			print('Wrong answer. returning...')
			return
		gv.BROADCAST_DELAY = value
	elif(variable == 'set_ip'):
		input_value = input('\t\tChoose IP>')	
		if(str(bytes(input_value, 'utf-8')) == "b''"): 
			print('returning')
			return
		value = str(input_value)
		if(ad.is_valid_ip(value)):
			gv.BROADCAST_IP_TO_SEND = value
		else:
			print('Wrong IP entered. returning...')
			return
	elif(variable == 'set_notifs'):
		input_value = input('\t\tChoose Value(T or F)>')	
		if(str(bytes(input_value, 'utf-8')) == "b''"): 
			print('returning')
			return
		value = str(input_value)
		if(value == 'T'):
			gv.BROADCAST_NOTIFICATION = True
		elif(value == 'F'):
			gv.BROADCAST_NOTIFICATION = False
		else:
			print('Wrong answer. returning...')
			return
	else:
		print('Wrong answer. returning...')
		return


def send_broadcast_message():
	send_single_broadcast_message()
	while True:
		if gv.SENDING_BROADCAST:
			send_single_broadcast_message()
		time.sleep(gv.BROADCAST_DELAY)


def send_single_broadcast_message():
	msg = gv.BROADCAST_IP_TO_SEND
	msg_bytes = bytes(msg, 'utf-8')
	dest = ('<broadcast>',10100)
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	if gv.BROADCAST_NOTIFICATION:
		print ("")
	try:
		s.sendto(msg_bytes, dest)
		if gv.BROADCAST_NOTIFICATION:
			print ("A broadcast message has been send.")
			print ("You can Stop sending broadcast using bc command")
	except socket.error as error:
		if gv.BROADCAST_NOTIFICATION:
			print('error:', error)
		pass
	if gv.BROADCAST_NOTIFICATION:
		print ("")