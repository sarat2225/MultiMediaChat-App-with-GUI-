import socket
import threading
import time
import sys
import os

HEADER = 64
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = sys.argv[1]
print(SERVER)
PORT = int(sys.argv[2])
FORMAT = 'utf-8'
ADDRESS = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER_TERMINATION_MESSAGE = "SERVER HOST TERMINATED"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

ClientList = []
ClientListLock = threading.Lock()

def send_message(connection,msg):
    msg = msg.encode(FORMAT)
    message_length = f"{len(msg):<{HEADER}}".encode(FORMAT)
    connection.send(message_length + msg)

def recv_message(connection):
    message_header = connection.recv(HEADER)
    message_length = int(message_header.decode(FORMAT).strip())
    msg = connection.recv(message_length).decode(FORMAT)
    return msg 

def recv_send_file(connection):
    file_size = int(recv_message(connection))

    print("recv_send_file : file_size : ",file_size)

    for c in ClientList:
        if c[0]==connection:
            continue
        send_message(c[0],str(file_size))
    
    temp_size=0
    while temp_size < file_size :
        #data = recv_message(connection)
        data = connection.recv(1024)
        temp_size += len(data)
        for c in ClientList:
            if c[0]==connection:
                continue

            c[0].send(data)

    print("recv_send sucessfull")
    

def GroupChatClient(connection,address):
    ClientNameMsg = recv_message(connection)
    print(ClientNameMsg)
    with ClientListLock :
        ClientList.append((connection,ClientNameMsg))

    with ClientListLock:
        for c in ClientList:
            if c[0]==connection : 
                continue
            send_message(c[0],f"{ClientNameMsg} joined the chat!")

    send_message(connection,str(len(ClientList)))
    for clients in ClientList :
        send_message(connection,clients[1])

    try:
        connected = True 
        while connected :
            msg = recv_message(connection)
            if not msg:
                break
            if msg == DISCONNECT_MESSAGE:
                with ClientListLock:
                    for c in ClientList:
                        if c[0]==connection :
                            continue
                        send_message(c[0],f"{ClientNameMsg} exited the chat")
                connected = False

            print(f"[{ClientNameMsg}] {msg}")
            with ClientListLock:
                for c in ClientList:
                    if c[0]==connection :
                        continue 
                    send_message(c[0],f"[{ClientNameMsg}] {msg}")

            if msg[0:6] == '!send ':
                recv_send_file(connection)
            
    finally :
        with ClientListLock :
            ClientList.remove((connection,ClientNameMsg))
        send_message(connection,msg)
        connection.close()
    


def StartServer():
    ClientList = []

    print('[SERVER LISTENING]')
    server.listen()

    try :
        while True:
            connection , address = server.accept()
            thread = threading.Thread(target=GroupChatClient
                                     ,args=(connection,address))
            thread.start()
            
    except KeyboardInterrupt: 
        server.close()
        print('[SERVER TERMINATED]')
        sys.exit()


print('[ACTIVATING SERVER]')
print("For Server Termination, use the Keyboard Interrupt (Ctrl-C)")
StartServer()
