#!/usr/bin/python3
import socket 
import threading
import concurrent.futures
import time

import global_variables as gv
import command_parser


def server_shell():
	print('Starting Shell...')
	time.sleep(0.2)
	while True:
		prompt = 'Enter Command (%s)>' % len(gv.CLIENTS)
		command = input(prompt)
		if(str(bytes(command, 'utf-8')) == "b''"): continue
		command_parser.parse_command(command)