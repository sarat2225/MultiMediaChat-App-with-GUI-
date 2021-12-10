## *CS3530: Computer Networks-1*

### **Multimedia Group Chat**

#### *Installation*

* Command for installation of python: ```sudo apt-get install python3```
* Command for installation of kivy  : ```pip3 install kivy```

#### *Commands for execution*

* Server : ```python3 server.py <Host_Name> <Port_Number>```
* Client : ```python3 client.py <Host_Name> <Port_Number>```

The hostname and port number of the server and client must be given as command line arguements.

#### *Keywords*

* ```!q```    - to get disconnected from the server
* ```!send``` - to send necesarry files
* ```!DICONNECT``` - client disconnection message

#### *Baseline Implementation*

* *__Text Chat__* : Clients can perform group chat by connecting to the server rather than connecting to each and every client.
* Simultaneous receiving and sending of messages in both Server and Client

### *Enhanced Version*

##### File Attachments

* Many file formats like .pdf,.zip,.pptx, etc., can be sent from one client to all other clients by the command  ```!send <filename>```
* Larger files are sent by splitting the file into smaller chunks.

##### Image, Video and Audio Sharing

* Image, video, and audio files can be shared from one client to all other clients by the command  ```!send <filename>```
* All Image formats like .jpg,.jpeg,.mpeg,.png, etc., are supported.
* All Video formats like .mp4,.mov, etc., are supported.
* All Audio formats like .mp3,.mp4, etc., are supported.

##### Graphic User Interface (GUI)

* We used GUI for a better interface and better readability for the user.
* GUI gives more functionality than CLI in terms of providing buttons and controlling thread processes efficiently
