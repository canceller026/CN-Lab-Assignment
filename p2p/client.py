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
        self.server_info = server_info  # Server Address
        self.name = peername if peername is not None else ':'.join((serverhost, serverport))
        self.connectable_peer = {}
        # example name: 192.168.0.1:30000
        msg_func_handle = {
            'CHAT': self.receive_message,
            'ACCEPT': self.chat_accept,
            'REFUSE': self.chat_refuse,
            'REQUEST': self.request,
            'REGISTER_SUCCESS': self.register_success,
            'REGISTER_ERROR': self.register_fail,
            'PEERLIST': self.display_all_peers,
            'DISCONNECT': self.disconnect,
            'FILE': self.file_transfer,
        }
        for message_type, func in msg_func_handle.items():
            self.func_assign(message_type, func)

        # Variable checking request status --None--True--False
        self.agree = None
        
        self.file_data = {}


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
    #REGISTER==============================================================================================================
    #Register
    def send_register(self):
        """ Send a request to server to register peer's information. """
        data = {
            'peername': self.name,
            'host': self.serverhost,
            'port': self.serverport
        }
        print(self.server_info)
        self.socket_sending(self.server_info, msgtype='REGISTER', msgdata=data)

    #Register success notification
    def register_success(self, msgdata):
        """ Processing received message from server: Successful registration on the server. """
        self.send_listpeer()  # Update connected peer table
        print('Register Successful.')
    #Register failed notification
    def register_fail(self, msgdata):
        """ Processing received message from server: Registration failed on the server. """
        print('Register Error.')
    #======================================================================================================================

    #SHOW PEER LIST =======================================================================================================
    #Request to see all peers
    def send_listpeer(self):
        """ Send a request to server to get all peers information. """
        data = {'peername': self.name}
        self.socket_sending(self.server_info, msgtype='PEERLIST', msgdata=data)    

    #Display all peers available
    def display_all_peers(self, msgdata):
        """ Processing received message from server:
            Output information about all peers that have been registered on the server. """
        self.connectable_peer = {key:tuple(value) for key, value in msgdata['peerlist'].items()}
        print('display all peers:')
        # print(msgdata['peerlist'])
        for peername, peer_info in msgdata['peerlist'].items():
            print('peername: ' + peername + '---' + peer_info[0] + ':' + str(peer_info[1]))
    
    #Show list connected peers
    def list_connected_peer(self):
        """ Output all connected peers information. """
        for peername, peer_info in self.peerlist.items():
            print('peername: ' + peername + '---' + peer_info[0] + ':' + str(peer_info[1]))
    #======================================================================================================================    
    
    #CHAT==================================================================================================================
    #Send request to peer to connect
    def send_request(self, peername):  
        """ Send a chat request to peer. """
        if peername not in self.peerlist:
            try:
                server_info = self.connectable_peer[peername]
            except KeyError: 
                print('This peer ({}) is not registered.'.format(peername))
            else:
                data = {
                    'peername': self.name,
                    'host': self.serverhost,
                    'port': self.serverport
                }
                self.socket_sending(server_info, msgtype='REQUEST', msgdata=data)
        else:
            print('You have already connected to {}.'.format(peername))

    #Accept and refuse request
    def chat_accept(self, msgdata):
        """ Processing received accept chat request message from peer.
            Add the peer to collection of connected peers. """
        peername = msgdata['peername']
        host = msgdata['host']
        port = msgdata['port']
        print('chat accept: {} --- {}:{}'.format(peername, host, port))
        self.peerlist[peername] = (host, port) 
    
    def chat_refuse(self, msgdata):
        """ Processing received refuse chat request message from peer. """
        print('CHAT REFUSE!')
    
    def accept_request(self):
        self.agree = True
    
    def refuse_request(self):
        self.agree = False
    
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

    #Send chat messages to peers -- many people
    def send_chat_messageS(self,peer:list, message):
        """ Send a chat message to peers. """
        for peername in peer:
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

    #LOG OUT =============================================================================================================
    #Send exit request
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
        print('1. REGISTER')
        print('2. SHOW PEER LIST ')
        print('3. SHOW CONNECTED PEER LIST')
        print('4. REQUEST')
        print('5. CHAT')
        print('6. CHAT ALL')
        print('7. SEND FILE')
        print('8. DISCONNECT PEER')
        print('9. EXIT NETWORK')
        print('10. EXIT SYSTEM')
        print('11. HELP MENU')
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
                case '1':
                    self.send_register()
                case '2':
                    self.send_listpeer()
                case '3':
                    self.list_connected_peer()
                case '4':
                    peername = input("Please input the peer you want to connect: ")
                    self.send_request(peername)
                case 'yes':
                    self.accept_request()
                case 'no':
                    self.refuse_request()
                case '5':
                    peername = input("Please input the peer you want to chat (seperated by space): ")
                    peer = peername.split(' ')
                    print(peer)
                    message = input("Type the message: ")
                    self.send_chat_messageS(peer, message)
                case '6':
                    message = input("Type the message: ")
                    self.send_chatall_message(message)
                case '7':
                    peername = input("Please input the peer you want to send file: ")
                    filename = input("Type the file path: ")
                    self.send_file(peername, filename)
                case '8':
                    peername = input("Please input the peer you want to disconnect: ")
                    self.send_disconnect(peername)
                case '9':
                    self.send_exit_network()
                case '10':
                    self.system_exit()
                case '11':
                    self.menu()


if __name__ == '__main__':
    serverport = int(input('Please choose a serverport (1024 -> 49151): '))
    peername = input('Type in your name: ')
    client = Client(peername=peername, serverport=serverport)
    client.run()
