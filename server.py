#!/usr/bin/python3
import socket 
import threading
import concurrent.futures
import time

import client_handler
import server_interactive_menu
import broadcast_handler



if __name__ == "__main__":
	with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
		executor.submit(client_handler.listen_to_new_clients)
		executor.submit(server_interactive_menu.server_shell)
		executor.submit(broadcast_handler.send_broadcast_message)