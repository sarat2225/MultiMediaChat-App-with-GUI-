import socket
import threading
import time
import sys
import os


HEADER = 64   # FOR MESSAGE LENGTH
PORT = 5050
SERVER = '192.168.0.101'
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER_TERMINATION_MESSAGE = "SERVER HOST TERMINATED"

ClientName = socket.gethostname()

ListenSendLock = threading.Lock()

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def send_message(connection,msg):
    msg = msg.encode(FORMAT)
    message_length = f"{len(msg):<{HEADER}}".encode(FORMAT)
    connection.send(message_length + msg)

def send_file(connection,msg):
    print("send_file_msg1 filename : ",msg[6:])
    filename = msg[6:]
    file_size = os.path.getsize(filename)
    print(file_size)
    print(os.path.basename(filename))
    #connection.send((str(file_size)).encode())
    send_message(connection,str(file_size))
    #print(os.path.isabs(filename))
    file = open(filename,"rb")
    temp_size = 0
    while temp_size < file_size :
        data = file.read(1024)
        if not data :
            break;

        connection.send(data)
        temp_size += len(data)
    print("File Successfully sent")

def recv_file(connection,msg):
    filePath = msg[6:]
    fileName = os.path.basename(filePath)
    print("recv_file_msg1 filename : ",)
    file = open(fileName,"wb")
    file_size = int(recv_message(connection))

    print("recv_file _msg2 file_size : ",file_size)

    temp_size=0
    while(temp_size < file_size):
        data = connection.recv(1024)
        temp_size += len(data)
        file.write(data)
    print("Succesfully recieved")


def recv_message(connection):
    message_header = connection.recv(HEADER)
    message_length = int(message_header.decode(FORMAT).strip())
    msg = connection.recv(message_length).decode(FORMAT)
    return msg 

def ListeningThread(connection):
    while True:
        msg = recv_message(connection)
        if msg == DISCONNECT_MESSAGE:
            break
        print(msg)

        index = msg.find(']')
        msg = msg[index+2:]
        if msg[0:6] == '!send ' :
            recv_file(connection,msg)

        
def TypingThread(connection):
    while True:
        msg = input()
        if msg == '!q':
            break
        send_message(connection, msg)

        if msg[0:6] == '!send ' :
            send_file(connection,msg)

    msg = DISCONNECT_MESSAGE    
    send_message(connection,msg)

    time.sleep(1)
    print('Disconnected')
    sys.exit()


def TerminalModeStart():
    connection = connect()
    Name = input("Enter your Name : ")
    
    send_message(connection,Name)

    ClientListCount = recv_message(connection)
    print("Total No of Clients: ",ClientListCount)
    for i in range(int(ClientListCount)):
        EachClient = recv_message(connection)
        print("Client ",i+1," : ",EachClient)
        
    ListenThread = threading.Thread(target=ListeningThread, args=(connection,))
    TypeThread   = threading.Thread(target=TypingThread, args=(connection,))
    ListenThread.start()
    TypeThread.start()

if __name__ == "__main__":
    TerminalModeStart()
