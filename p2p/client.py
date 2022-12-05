import socket
import threading
import time
IP_ADDRESS = "191.16.15.62"

def main():

    # Create client IPV4 and TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect with client address
    try:
        client.connect((IP_ADDRESS, 7777))
    except:
        return print('\n Cant connect to server\n')

    # Enter your name
    print('\n\n ====== ' + 'Welcome to the chat' + '!'':) ' + '======')
    time.sleep(1)
    print('\nEnter your name here.' )
    user = input('User ' )
    print('\nYou will be connected soon'';)')

    for i in range(0, 3):
        print('.')
        time.sleep(2)

    print('\nConnected.')
    print('===============================')
    print(f'\n{user} ' + 'are in the chat now.')

    
    thread_receive = threading.Thread(target=Receive_message, args=[client])
    thread_send = threading.Thread(target=Sending_message, args=[client, user])

    thread_receive.start()
    thread_send.start()


# Receive message function
def Receive_message(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg+'\n')
        except:
            print('\n User disconnected.\n')
            print('Press <Enter> to continue.')
            client.close()
            break

# Sending message function
def Sending_message(client, user):
    check = False
    while True:
        try:
            if(check == False):
                msg = user + ' are in the chat now.'
                client.send(f'{msg}\n'.encode('utf-8'))
                check = True
            else:
                msg = input('\n')
                client.send(f'{user}: {msg}'.encode('utf-8'))
        except:
            return

#run this function
main()