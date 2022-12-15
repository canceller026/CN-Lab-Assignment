import os
import socket
import sys
import json
import threading
import time
import atexit

from math import ceil
from base import Peer


class Client(Peer):
    def __init__(self, peername=None, serverhost='localhost', serverport=40000, server_info=('localhost', 30000)): #custom server ip
        super(Client, self).__init__(serverhost, serverport)
        self.socket.listen()
        self.server_info = server_info  # Server Address
        self.name = peername if peername is not None else ':'.join((serverhost, serverport))
        self.connectable_peer = {}
        friendlist:list = []
        # example name: 192.168.0.1:30000
        msg_func_handle = {
            'CHAT': self.receive_message,
            'ACCEPT': self.chat_accept,
            'REFUSE': self.chat_refuse,
            'REQUEST': self.request,
            'LOGIN_SUCCESS': self.login_success,
            'LOGIN_ERROR': self.login_fail,
            'REGISTER_SUCCESS': self.register_success,
            'REGISTER_ERROR': self.register_fail,
            'PEERLIST': self.display_all_peers,
            'ADD_FRIEND_REQUEST':self.receive_addfriend,
            'ADD_FRIEND_ACCEPT':self.addfriend_accept,
            'ADD_FRIEND_REFUSE':self.addfriend_refuse,
            'DISCONNECT': self.disconnect,
            'FILE': self.file_transfer,
        }
        for message_type, func in msg_func_handle.items():
            self.func_assign(message_type, func)

        # Variable checking request status --None--True--False
        self.agree = None
        
        self.file_data = {}

    #REGISTER =============================================================================================================
    def send_register(self):
        """ Send a request to server to login peer's information. """
        data = {
            'peername': self.name,
            'host': self.serverhost,
            'port': self.serverport,
            'friend':f"{self.name}"
        }
        print(self.server_info)
        self.socket_sending(self.server_info, msgtype='REGISTER', msgdata=data)

    #register success notification
    def register_success(self, msgdata):
        """ Processing received message from server: Successful registration on the server. """
        self.send_listpeer()  # Update connected peer table
        print('register Successful.')

    #register failed notification
    def register_fail(self, msgdata):
        """ Processing received message from server: Registration failed on the server. """
        print('register Error.')
    #======================================================================================================================

    #LOGIN=================================================================================================================
    def send_login(self):
        """ Send a request to server to login peer's information. """
        data = {
            'peername': self.name,
            'host': self.serverhost,
            'port': self.serverport
        }
        connect = {'msg':'Hello from ' + self.name + ':' + str(self.serverhost) + " - " + str(self.serverport)}
        print(self.server_info)
        self.socket_sending(self.server_info, msgtype='LOGIN', msgdata=data)
        self.server_sending(self.server_info, msgtype='CONNECT', msgdata = connect)
        

     #login success notification
    def login_success(self, msgdata):
        """ Processing received message from server: Successful registration on the server. """
        self.friendlist = msgdata["friend"].split(', ')
        print(self.friendlist)
        print('login Successful.')
        self.send_listpeer()

    #login failed notification
    def login_fail(self, msgdata):
        """ Processing received message from server: Registration failed on the server. """
        print('login Error.')
    #======================================================================================================================

    #SHOW PEER LIST =======================================================================================================
    def send_listpeer(self):
        """ Send a request to server to get all peers information. """
        data = {'peername': self.name}
        self.socket_sending(self.server_info, msgtype='PEERLIST', msgdata=data)

    def send_listpeer1(self):
        """ Send a request to server to get all peers information. """
        data = {'peername': self.name}
        self.socket_sending(self.server_info, msgtype='PEERLIST', msgdata=data)

    #Display all peers available
    def display_all_peers(self, msgdata):
        """ Processing received message from server:
            Output information about all peers that have been logined on the server. """
        self.connectable_peer = {key:tuple(value) for key, value in msgdata['peerlist'].items()}
        print('display all peers:')
        # print(msgdata['peerlist'])
        for peername, peer_info in msgdata['peerlist'].items():
            print('peername: ' + peername)

    #Display all peers available
    def display_all_peers1(self, msgdata):
        """ Processing received message from server:
            Output information about all peers that have been logined on the server. """
        self.connectable_peer = {key:tuple(value) for key, value in msgdata['peerlist'].items()}
        print('display all peers:')
        # print(msgdata['peerlist'])
        for peername, peer_info in msgdata['peerlist'].items():
            print('peername: ' + peername + ' : ' + peer_info["port"])

    #Show list connected peers
    def friend_list(self):
        """ Output all connected peers information. """
        print(self.friendlist)

    #Show list connected peers
    def list_connected_peer(self):
        """ Output all connected peers information. """
        for peername, peer_info in self.peerlist.items():
            print('peername: ' + peername + '---' + peer_info[0] + ':' + str(peer_info[1]))
    #======================================================================================================================  

    #ADD FRIEND============================================================================================================
    def send_addfriend(self, peername):
        if peername not in self.friendlist:
            try:
                server_info = self.connectable_peer[peername]
            except KeyError: 
                print('This peer ({}) is not logined.'.format(peername))
            else:
                data = {
                    'peername': self.name,
                    'host': self.serverhost,
                    'port': self.serverport
                }
                self.socket_sending(server_info, msgtype='ADD_FRIEND_REQUEST', msgdata=data)
        else:
            print('You are already friend with {}.'.format(peername))

     #Receive chat message request
    def receive_addfriend(self, msgdata):
        """ Processing received chat request message from peer. """
        peername = msgdata['peername']
        host, port = msgdata['host'], msgdata['port']
        print('addfriend request from: {} --- {}:{}'.format(peername, host, port))
        print('Please enter "yes" or "no":')

        while self.agree is None:  # Check answer
            time.sleep(0.1)
        #ACCEPT
        if self.agree is True:
            self.agree = None
            data = {
                'peername': self.name,
                'host': self.serverhost,
                'port': self.serverport,
                'host_send':host,
                'port_send':port,
                'username_send':peername
            }
            self.socket_sending(self.server_info, msgtype='ACCEPT_ADDFRIEND', msgdata=data)
        #REFUSE
        elif self.agree is False:
            self.agree = None
            self.socket_sending((host, port), msgtype='REFUSE', msgdata={})

    def addfriend_accept(self, msgdata):
        """ Processing received accept chat request message from peer.
            Add the peer to collection of connected peers. """
        username = msgdata['username_send']
        host = msgdata['host_send']
        port = msgdata['port_send']
        friend = msgdata['friend_send']
        print('add friend request accept: {} --- {}:{}'.format(username, host, port))
        print(friend.split(', '))
        self.send_login()

    def addfriend_refuse(self, msgdata):
        """ Processing received refuse chat request message from peer. """
        print('ADD FRIEND REFUSE!')

    def accept_request(self):
        self.agree = True
        self.send_login()
    
    def refuse_request(self):
        self.agree = False
    #======================================================================================================================  
    
    #REQUEST===============================================================================================================
    def send_chat_request(self, peername):
        """ Send a chat request to peer. """
        if peername not in self.peerlist and peername in self.friendlist:
            try:
                server_info = self.connectable_peer[peername]
            except KeyError: 
                print('This peer ({}) is not registered or not one of your friend.'.format(peername))
            else:
                data = {
                    'peername': self.name,
                    'host': self.serverhost,
                    'port': self.serverport
                }
                self.socket_sending(server_info, msgtype='REQUEST', msgdata=data)
        else:
            print('You have already connected to {}.'.format(peername))

    #Receive chat message request
    def request(self, msgdata):
        """ Processing received chat request message from peer. """
        peername = msgdata['peername']
        host, port = msgdata['host'], msgdata['port']
        print('request: {} --- {}:{}'.format(peername, host, port))
        print('Please enter "yes" or "no":')

        while self.agree is None:  # Check answer
            time.sleep(0.1)
        #ACCPEPT
        if self.agree is True:
            self.agree = None
            data = {
                'peername': self.name,
                'host': self.serverhost,
                'port': self.serverport
            }
            self.socket_sending((host, port), msgtype='ACCEPT', msgdata=data)
            self.peerlist[peername] = (host, port)
        #REFUSE
        elif self.agree is False:
            self.agree = None
            self.socket_sending((host, port), msgtype='REFUSE', msgdata={})

    #Accept request
    def chat_accept(self, msgdata):
        """ Processing received accept chat request message from peer.
            Add the peer to collection of connected peers. """
        peername = msgdata['peername']
        host = msgdata['host']
        port = msgdata['port']
        print('chat accept: {} --- {}:{}'.format(peername, host, port))
        self.peerlist[peername] = (host, port)
        self.send_listpeer()
    
    #Refuse request
    def chat_refuse(self, msgdata):
        """ Processing received refuse chat request message from peer. """
        print('CHAT REFUSE!')
    
    def accept_request(self):
        self.agree = True
        self.send_listpeer()
    
    def refuse_request(self):
        self.agree = False
    #======================================================================================================================
    
    #CHAT==================================================================================================================
    #Send chat message -- 1person
    def send_chat_message(self, peername, message):
        """ Send a chat message to peer. """
        try:
            peer_info = self.peerlist[peername]
        except KeyError:
            print('chat message: Peer does not exist.')
        else:
            data = {
                'peername': self.name,
                'message': message
            }
            self.socket_sending(peer_info, msgtype='CHAT', msgdata=data)

    #Send all chat message -- all
    def send_chatall_message(self, message):
        """ Send a chat message to peer. """
        for peername in self.peerlist:
            try:
                peer_info = self.peerlist[peername]
            except KeyError:
                print('chat message: Peer does not exist.')
            else:
                data = {
                    'peername': self.name,
                    'message': message
                }
                self.socket_sending(peer_info, msgtype='CHAT', msgdata=data)

     #Receive message from others
    def receive_message(self, msgdata):
        """ Processing received chat message from peer."""
        peername = msgdata['peername']
        if peername in self.peerlist:
            print(peername +' : '+ msgdata['message'])
            # return self.message_format.format(peername=peername, message=msgdata['message'])
    #======================================================================================================================

    #FILE TRANSFER ========================================================================================================
    def file_transfer(self, msgdata):
        peername = msgdata['peername']
        filename = msgdata['filename']
        filenum = int(msgdata['filenum'])
        curnum = int(msgdata['curnum'])
        filedata = msgdata['filedata']
        
        key = peername + '_' + filename
        if self.file_data.get(key) is None:
            self.file_data[key] = [None] * filenum
        self.file_data[key][curnum] = filedata
        print(self.file_data[key])

    def send_file(self, peername, filename):
        try:
            peer_info = self.peerlist[peername]
        except KeyError:
            print("send file: Peer does not exist.")
        else:
            read_per = 128
            tmp_text = []
            with open(filename, 'rt', encoding='utf-8') as f:
                while True:
                    text_data = f.read(read_per)
                    if not text_data:
                        break
                    tmp_text.append(text_data)
            tran_num = len(tmp_text)
            for index, item in enumerate(tmp_text):
                data = {
                    'peername': self.name,
                    'filename': filename,
                    'filenum': tran_num,
                    'curnum': index,
                    'filedata': item
                }
                self.socket_sending(peer_info, msgtype='FILE', msgdata=data)
    #======================================================================================================================

    #DISCONNECT BETWEEN PEERS ============================================================================================= 
    #Send disconnect request
    def send_disconnect(self, peername):
        """ Send a disconnect request to peer. """
        try:
            peer_info = self.peerlist[peername]
        except KeyError:
            print('disconnect: Peer does not exist.')
        else:
            del self.peerlist[peername]
            data = {'peername': self.name}
            self.socket_sending(peer_info, msgtype='DISCONNECT', msgdata=data)

    #Peer disconnect receive message
    def disconnect(self, msgdata):
        """ Processing received messages from peer:
            Disconnect from the peer. """
        peername = msgdata['peername']
        if peername in self.peerlist:
            print('Disconnected from {}'.format(peername))
            del self.peerlist[peername]   
    #======================================================================================================================

    #LOG OUT ==============================================================================================================
    def send_exit_network(self):
        """ Send a request to server to quit P2P network. """
        data = {'peername': self.name}
        self.socket_sending(self.server_info, msgtype='EXIT_NETWORK', msgdata=data)

    #Stop program
    def system_exit(self):  # Logout network
        for peername in self.peerlist:  # Disconnect connected peers
            # Prevent interuption
            try:
                self.send_disconnect(peername)
            except ConnectionRefusedError:
                pass
            except:
                pass
        try:
            self.send_exit_network()  # Log out before exit program cuz no db stored
        except ConnectionRefusedError:
            pass
        except:
            pass
        sys.exit()    
    #======================================================================================================================

    # MENU ================================================================================================================
    def menu(self):
        print('command list:')
        print('0. REGISTER')
        print('1. LOGIN')
        print('2. SHOW ONLINE PEER LIST ')
        print('3. ADD FRIEND')
        print('4. SHOW FRIEND LIST')
        print('5. CHAT REQUEST')
        print('6. SHOW LIST CONNECTED PEER')
        print('7. CHAT')
        print('8. CHAT ALL')
        print('9. SEND FILE')
        print('10. DISCONNECT PEER')
        print('11. EXIT NETWORK')
        print('12. EXIT SYSTEM')
        print('13. HELP MENU')
        
    #======================================================================================================================
    # Analyze the cmd input and direct it to the mapping function
    def run(self):
        atexit.register(client.system_exit)  # Prevent program being interupt and cannot exit
        
        t = threading.Thread(target=self.receive)  
        t.daemon=True
        t.start()
        
        self.menu()
        while True:
            option = input("please choose an option : \n")
            match option:
                case '0':
                    self.send_register()
                case '1':
                    self.send_login()
                case '2':
                    self.send_listpeer()
                case '3':
                    peername = input("Please input the username you want to add friend: ")
                    self.send_addfriend(peername)
                case 'yes':
                    self.accept_request()
                case 'no':
                    self.refuse_request()
                case '4':
                    self.friend_list()
                case '5':
                    peername = input("Please input the peer you want to connect: ")
                    self.send_listpeer()
                    self.send_chat_request(peername)
                case '6':
                    self.list_connected_peer()
                case '7':
                    peername = input("Please input the peer you want to chat: ")
                    while True:
                        message = input("Type the message <Type [!END] to stop chat> : ")
                        if message == '!END':
                            break
                        elif message == '!SWITCH':
                            message = ""
                            peername = input("Please input the peer you want to chat: ")
                        self.send_chat_message(peername, message)
                case '8':
                    message = input("Type the message: ")
                    self.send_chatall_message(message)
                case '9':
                    peername = input("Please input the peer you want to send file: ")
                    filename = input("Type the file path: ")
                    self.send_file(peername, filename)
                case '10':
                    peername = input("Please input the peer you want to disconnect: ")
                    self.send_disconnect(peername)
                case '11':
                    self.send_exit_network()
                case '12':
                    self.system_exit()
                case '13':
                    self.menu()



if __name__ == '__main__':
    while True:
        try:
            serverport = int(input('Please choose a serverport (1024 -> 49151): '))
            peername = input('Type in your name: ')
            client = Client(peername=peername, serverport=serverport)
            client.run()
        except WindowsError as e:
            if e.winerror == 10048:
                print('ERROR when using username or port')
                print('Please redo in again')