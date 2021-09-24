#!/usr/bin/python3
import socket
import threading
import concurrent.futures
import time

import client_handler
import server_interactive_menu
import broadcast_handler
import global_variables as gv


if __name__ == "__main__":
    local_ip = socket.gethostbyname(socket.gethostname())
    # ================================================
    local_ip = '193.151.130.168'
    # ================================================
    local_ip_prompt = 'Please enter your ip address: [{}] '.format(local_ip)
    user_input = input(local_ip_prompt)
    if(not str(bytes(user_input, 'utf-8')) == "b''"):
        local_ip = str(user_input)

    gv.LOCAL_HOST = local_ip
    gv.BROADCAST_IP_TO_SEND = local_ip

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(client_handler.listen_to_new_clients)
        executor.submit(server_interactive_menu.server_shell)
        executor.submit(broadcast_handler.send_broadcast_message)
