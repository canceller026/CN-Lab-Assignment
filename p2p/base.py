import json
import socket


class Peer(object):
    """ Implements the core functionality that might be used by a peer in a P2P networks. """
    

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
            s.send( msg)
        finally:
            s.close()

    @staticmethod
    def socket_connect(address, msgtype, msgdata):
        """ Send JSON serialized data over a new TCP connection. """
        msg = {'msgtype': msgtype, 'msgdata': msgdata}
        msg = json.dumps(msg).encode('utf-8')
        # import pdb; pdb.set_trace()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(address)
        s.send(msg)
