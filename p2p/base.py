import json
import socket


class Peer(object):
    """ Implements the core functionality that might be used by a peer in a P2P networks. """
    def __init__(self, serverhost='localhost', serverport=13999, listen_num=100):
        self.serverhost, self.serverport = serverhost, int(serverport)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((serverhost, int(serverport)))
        self.socket.listen(listen_num)
        self.peerlist = {}
        self.msg_func_handle = {}
    
    def func_assign(self, message_type, func):
        self.msg_func_handle[message_type] = func
    
    def classifier(self, msg):
        type_ = msg['msgtype']
        data_ = msg['msgdata']
        self.msg_func_handle[type_](data_)
    
    def receive(self):
        while True:  #--
            conn, addr = self.socket.accept()
            buf = conn.recv(2048)
            msg = json.loads(buf.decode('utf-8'))
            self.classifier(msg)

    #Sending data between server and clients / protocol
    @staticmethod
    def socket_sending(address, msgtype, msgdata):
        """ Send JSON serialized data over a new TCP connection. """
        msg = {'msgtype': msgtype, 'msgdata': msgdata}
        msg = json.dumps(msg).encode('utf-8')
        # import pdb; pdb.set_trace()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(address)
        except ConnectionRefusedError:
            print('CONNECTING ERROR : MAKE SURE THE OTHERSIDE IS ACTIVE')
            raise
        else:
            s.send(msg)
        finally:
            s.close()
