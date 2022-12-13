import socket
import json
import threading

from base import Peer

class Server(Peer):
    """ Server implementation of P2P chat system. """
    def __init__(self, serverhost='localhost', serverport=30000): #server IP
        super(Server, self).__init__(serverhost, serverport)
        msg_func_handle = {
            'REGISTER': self.register,
            'PEERLIST': self.listpeer,
            'EXIT_NETWORK': self.exit_network,
        }
        for message_type, func in msg_func_handle.items():
            self.func_assign(message_type, func)      

    def exit_network(self, msgdata):
        peername = msgdata['peername']
        if peername in self.peerlist:
            del self.peerlist[peername]

    def register(self, msgdata):
        peername = msgdata['peername']
        host = msgdata['host']
        port = msgdata['port']
        if peername in self.peerlist:  # Name already taken
            self.socket_sending((host, port), msgtype='REGISTER_ERROR', msgdata={})
        else:
            self.peerlist[peername] = (host, port)
            self.socket_sending(self.peerlist[peername], msgtype='REGISTER_SUCCESS', msgdata={})

    def listpeer(self, msgdata):  
        peername = msgdata['peername']
        if peername in self.peerlist:
            data = {'peerlist': self.peerlist}
            self.socket_sending(self.peerlist[peername], msgtype='PEERLIST', msgdata=data)

    

    def run(self):
        t = threading.Thread(target=self.receive)
        t.daemon = True
        t.start()
        print("Type <end server> to stop the server.")
        while True:
            cmd = input()
            if cmd=='end server':
                break


if __name__ == '__main__':
    server = Server()
    print(server.socket)
    server.run()
