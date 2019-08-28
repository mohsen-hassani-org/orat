import socket

import command_parser
import global_variables as gv



def listen_to_new_clients():
	print('Listen for new clients')
	try:
		s = socket.socket()
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((gv.LOCAL_HOST, gv.PORT))
		s.listen(5)
	except socket.error as ex:
		print(ex)
		pass
	print('Wiating for clients')
	while True:
		c, addr = s.accept()
		client_info = command_parser.request_client_info(c)
		gv.CLIENTS.append({
			'client': c, 
			'address': addr, 
			'client_info': client_info
			})
		print ('Got new connection from', addr, 'info:' , client_info)
