# CN-Lab-Assignment
# Chat application

It is a hybrid chat application between client-server and peer-to-peer (P2P).<br/>

![Model](model.png)
* Client-Server :
    * **Accounts registration**<br/>
    Users can create new account by make a registration or simple login into the network using their account.
    * **Login and Logout**<br/>
    When a user logs in, the server will saves their ip address and port number into database and this entry stays in the database until the user logs out or disconnected from the network.<br/>Whenever a login request is sent to the server, a message will be sent from the client-side to the server-side to notificate that they have made a connection.
    * **Info-retrieve request**<br/>
    A user can find information of another online user using that user's username to retrieve the ip address and the port number of the users who are currently active from the server.
* P2P:
    * **Add friend**<br/>
    A user can send an add-friend request to others. Client can only chat when they already have been friend.
    * **Chat**<br/>
    When a user wants to chat with another user, a chat request is sent to the other user. If that user accept the request, the conversation could begin and vice versa.
    * **Chat all**<br/>
    A user can also send a message to all of the clients who are currently active and chat-request-accepted in the network.
     * **Send file**<br/>
    User can also sending file to others. The file received will be displayed in format [filename]:[file content]..
    

## How to Use It?
First, clone the repository
```
git clone https://github.com/canceller026/CN-Lab-Assignment.git
```
Then start the server
```
cd p2p
python server.py
```

Install pyqt5 package before start the chat application
```
cd p2p
pip install pyqt5
python main.py
```

Finally, register/login and start chatting with your friends.
