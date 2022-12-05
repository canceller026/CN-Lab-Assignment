import threading  # Using multi-thread
import socket
from datetime import datetime

# create a list of user
clients = []
total = 0
m = []
count = 0
# main function


def main():
    global count
    global total
    daytime = datetime.now().strftime('%d/%m/%Y %H:%M')

    # create object to pass parameter : address, TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    try:
        server.bind((socket.gethostbyname(socket.gethostname()), 7777))
        server.listen()  # Server is now ready to connect
        print(f'\nOpen chat on {daytime}')
        print("Wait for clients to connect")
    except:
        #  Cant connect to the server
        return print('\nCant start server\n')

    # Accept connection
    while True: 
        client, addr = server.accept()  # Connection return addresses
        clients.append(client)  # Add client into client list
        total = total + 1
        print('\nNew client is ' + 'CONNECTED. ' + f'Total: {total} clients!')

        if count != 0:
            client.send(bytes('\n', encoding="utf-8"))
            for i in range(count):
                client.send(m[i])
                client.send(bytes('\n\n', encoding="utf-8"))

        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()


def messagesTreatment(client):  # Listen to client's chat
    global count
    check = False
    while True:
        try:
            if(check == False):
                nome = client.recv(2048)
                broadcast(nome, client)
                check = True
            else:
                msg = client.recv(2048)
                count = count + 1
                m.append(msg)
            # Messages are send to all clients
                broadcast(msg, client)
        except:
            deleteClient(client)
            break 


def broadcast(msg, client):
    for clientItem in clients: 
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                deleteClient(clientItem)


def deleteClient(client):
    global total
    global count
    total = total - 1
    if total == 0:
        print('\nA client has' + ' DISCONNECTED. ' + f'Total: {total} members!')
        print('\nThere is no clients in the chat now')
        m.clear()
        count = 0
    else:
        print('\nA client has' + ' DISCONNECTED. ' + f'Total: {total} members!')

    clients.remove(client)

#run this function
main()