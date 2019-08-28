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
	print('Variable\tVlaue\t\tDescription')
	print('------------------------------------------------------------------------')
	print('bc_flag\t\t%s\t\tSet True to send broadcast messages. False to disable it' % gv.SENDING_BROADCAST)
	print('bc_delay\t%s\t\tDelay beetwen sending broadcast messages (Sec)' % gv.BROADCAST_DELAY)
	print('bc_ip\t\t%s\tIP Address to send as broadcast' % gv.BROADCAST_IP_TO_SEND)
	print('')
	print('')
	print("set_flag \t - Stop or Start sending broadcast messages on the network")
	print("set_delay \t - Set delay beetwen sending broadcast messages (Sec)")
	print("set_ip \t\t - IP to send broadcast on network")
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
	else:
		print('Wrong answer. returning...')
		return


def send_broadcast_message():
	while True:
		if gv.SENDING_BROADCAST:
			msg = gv.BROADCAST_IP_TO_SEND
			msg_bytes = bytes(msg, 'utf-8')
			dest = ('<broadcast>',10100)
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
			s.sendto(msg_bytes, dest)
			print ("")
			# print ("A broadcast message has been send.")
			# print ("You can Stop sending broadcast using bc command")
		time.sleep(gv.BROADCAST_DELAY)
