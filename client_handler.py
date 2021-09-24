import socket

import command_parser
import global_variables as gv


def listen_to_new_clients():
    print('Listen for new clients on {} port {}'.format(gv.LOCAL_HOST, gv.PORT))
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
        client, addr = s.accept()
        print('\nGot new connection')
        client_info = command_parser.request_client_caption(client)
        gv.CLIENTS.append({
            'client': client,
            'address': addr,
            'client_info': client_info
        })
        print('New connection addr:', addr, 'info:', client_info)
