from socket import *
import json
from utils import Roles as RolesModule

serverPort = 4000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)  # Listen for incoming connections
print('Welcome to Broadcast Server')

# List of peers
listPeerListener = []

while True:
    connectionSocket, clientAddress = serverSocket.accept()
    clientMessage = connectionSocket.recv(2048)
    clientMessage = json.loads(clientMessage.decode())
    
    print('From: ', clientAddress)
    print('Message: ', clientMessage)

    # If message is from speaker, broadcast to all listeners
    if clientMessage["Header"]["Role"] == RolesModule.Roles.SPEAKER.value:
        for peer in listPeerListener:
            # Protocol
            message = {
                "Header": {
                    "Status": 200,
                    "Status Phrase": "OK",
                    "From": clientAddress,
                    "Role": RolesModule.Roles.SPEAKER.value
                },
                "Body": {
                    "Message": clientMessage["Body"]["Message"]
                }
            }
            # Convert the message to JSON string
            message = json.dumps(message)
            # Send the message to each peer
            try:
                peer.send(message.encode())
            except Exception as e:
                print(f"Error sending message to {peer}: {e}")

        # Protocol
        message = {
            "Header": {
                "Status": 200,
                "Status Phrase": "OK",
                "From": clientAddress,
                "Role": RolesModule.Roles.SERVER.value
            },
            "Body": {
                "Message": "Broadcast Success"
            }
        }
        
        # Convert the message to JSON string
        message = json.dumps(message)
        
        # Send to the speaker
        connectionSocket.sendall(message.encode())
        
    # If message is from listener, reply to the listener
    elif clientMessage["Header"]["Role"] == RolesModule.Roles.LISTENER.value:
        if connectionSocket not in listPeerListener:
            listPeerListener.append(connectionSocket)
            print('New peer added: ', clientAddress)
        
        # Protocol
        message = {
            "Header": {
                "Status": 200,
                "Status Phrase": "OK",
                "From": clientAddress,
                "Role": RolesModule.Roles.SERVER.value
            },
            "Body": {
                "Message": "Connection Success"
            }
        }
        
        # Convert the message to JSON string
        message = json.dumps(message)
        
        # Send to the listener
        connectionSocket.send(message.encode())
