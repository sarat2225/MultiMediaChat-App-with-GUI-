import kivy
kivy.require('1.0.7')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.label import Label


Builder.load_file('GroupChat.kv')

import clientHelper
import sys
import os
import threading
import time

connection = None
WindowPopup = None
Page = None
process_incomplete = True

class FileSelectLayout(Widget):
    FilePath = ObjectProperty(None)
    FileName = None
    defaultPath = os.path.expanduser("~/Desktop")
    def selected(self,filename):
        self.FileName = filename
    def select_event(self):
        print(self.FileName[0])
        global WindowPopup
        msg = "!send " + str(self.FileName[0])
        clientHelper.send_message(connection,msg)
        clientHelper.send_file(connection,msg)
        WindowPopup.dismiss()
        WindowPopup = None
    def cancel_event(self):
        global WindowPopup 
        WindowPopup.dismiss()
        WindowPopup = None

class MyFloatLayout(Widget):
    message = ObjectProperty(None)
    def message_send(self):
        message = self.message.text

        clientHelper.send_message(connection,message)
        global Page
        message = "[You] " + message
        Page.ids.ChatPage.text += message + "\n\n"
        self.message.text = ""
    def file_send(self):
        obj = FileSelectLayout()
        global WindowPopup 
        WindowPopup = Popup(title="Select File", content=obj,auto_dismiss = False)
        WindowPopup.open()

class GroupMediaChat(App):

    def on_stop(self):
        clientHelper.send_message(connection,clientHelper.DISCONNECT_MESSAGE)
        global process_incomplete
        process_incomplete = False
    def build(self):
        global Page
        Page = MyFloatLayout()
        return Page

def ListeningThread(connection):
    while process_incomplete:
        msg = clientHelper.recv_message(connection)
        if msg == clientHelper.DISCONNECT_MESSAGE:
            break
        global Page
        Page.ids.ChatPage.text += msg + "\n\n"
        index = msg.find(']')
        msg = msg[index+2:]
        if msg[0:6] == '!send ' :
            clientHelper.recv_file(connection,msg)

answer = input('Would you like to connect (yes/no)? ')
if answer.lower() != 'yes':
    sys.exit()

SERVER = sys.argv[1]
PORT = int(sys.argv[2])
ADDR = (SERVER, PORT)

clientHelper.SERVER = SERVER
clientHelper.PORT = PORT
clientHelper.ADDR = ADDR

print("Enter your preference mode:")
print("1.Terminal Mode")
print("2.GUI Mode")
i = int(input())


if(i == 1):
    clientHelper.TerminalModeStart()
elif(i == 2):
    connection = clientHelper.connect()
    Name = input("Enter your Name : ")
    clientHelper.send_message(connection,Name)
    ClientListCount = clientHelper.recv_message(connection)
    for i in range(int(ClientListCount)):
        EachClient = clientHelper.recv_message(connection)
    print(ClientListCount)
    app = GroupMediaChat()
    GuiThread = threading.Thread(target=app.run)
    ListenThread = threading.Thread(target=ListeningThread, args=(connection,))
    GuiThread.start()
    time.sleep(1)
    ListenThread.start()
    ListenThread.join()
else:
    print("Enter Choice correctly")