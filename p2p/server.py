import socket
import json
import threading
from base import Peer
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://thoxoantit2410:trungchanh2410@p2p-chat.psyodx0.mongodb.net/?retryWrites=true&w=majority")
db = cluster["P2P-chat"]
collection = db["userlist"]

class Server(Peer):
    """ Server implementation of P2P chat system. """
    def __init__(self, serverhost='localhost', serverport=30000): #server IP
        super(Server, self).__init__(serverhost, serverport)
        msg_func_handle = {
            'REGISTER': self.register,
            'LOGIN': self.login,
            'ACCEPT_ADDFRIEND':self.accept_addfriend,
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
        username = msgdata['peername']
        host = msgdata['host']
        port = msgdata['port']
        friend= msgdata['friend']
        if collection.find_one({"username":username}):  # Name already taken
            self.socket_sending((host, port), msgtype='REGISTER_ERROR', msgdata={})
        else:
            user = {"username":username, "host":host, "port":port, "friend":friend}
            collection.insert_one(user)
            self.peerlist[username] = (host, port)
            self.socket_sending(self.peerlist[username], msgtype='REGISTER_SUCCESS', msgdata={})

    def login(self, msgdata):
        username = msgdata['peername']
        host = msgdata['host']
        port = msgdata['port']
        friend = ""
        results = collection.find({"username":username})
        for result in results:
            friend = result["friend"]
        if collection.find({"username":username}):
            collection.update_one({"username":username}, {"$set":{"host":host, "port":port}})
            data = {'friend':friend}
            self.peerlist[username] = (host, port)
            self.socket_sending(self.peerlist[username], msgtype='LOGIN_SUCCESS', msgdata=data)
        else:
            self.socket_sending((host, port), msgtype='LOGIN_ERROR', msgdata={})

    def listpeer(self, msgdata):  
        peername = msgdata['peername']
        if peername in self.peerlist:
            data = {'peerlist': self.peerlist}
            self.socket_sending(self.peerlist[peername], msgtype='PEERLIST', msgdata=data)

    
    def accept_addfriend(self, msgdata):
        username = msgdata['peername']
        host = msgdata['host']
        port = msgdata['port']
        host_send = msgdata['host_send']
        port_send = msgdata['port_send']
        username_send = msgdata['username_send']
        content = ""
        content2 = ""
        peer = collection.find({"username":username})
        peer_send = collection.find({"username":username_send})
        for x in peer:
            content = x["friend"]
        collection.update_many({"username":username},{"$set":{"friend":content + ", " + username_send}})
        for x in peer_send:
            content2 = x["friend"]
        collection.update_many({"username":username_send},{"$set":{"friend":content2 + ", " + username}})
        for x in peer:
            content = x["friend"]
        for x in peer_send:
            content2 = x["friend"]
        data = {'host_send':host, "port_send":port, "username_send":username, "friend_send":content2}
        print(data)
        self.socket_sending((host_send, port_send), msgtype='ADD_FRIEND_ACCEPT', msgdata=data)


    def run(self, mode = 0):
        t = threading.Thread(target=self.receive)
        t.daemon = True
        t.start()
        print("Type <end server> to stop the server.")
        result = collection.find({"username":"trungchanh"})
        for results in result:
            print(results["host"])
        if (mode == 1):
            print("DEBUG_MODE: ON")
            while True:
                cmd = input()
                if cmd=='end server':
                    break
                if cmd == 'listpeer':
                    print(self.listpeer)


if __name__ == '__main__':
    server = Server()
    print(server.socket)
    server.run(1)
