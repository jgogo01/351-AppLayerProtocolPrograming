from socket import *
import json
from utils import Roles as RolesModule

serverPort = 4000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('Welcome to Broadcast Server')

# List of peers
listPeerListener = []

while True:
    clientMessage, clientAddress = serverSocket.recvfrom(2048)
    print('From: ', clientAddress)
    print('Message: ', clientMessage.decode())
    clientMessage = json.loads(clientMessage.decode())

    # If message is from speaker, broadcast to all listeners
    if clientMessage["Header"]["Role"] == RolesModule.Roles.SPEAKER.value:
        for peer in listPeerListener:
            if peer != clientAddress:
                # Protocol
                message = {
                    "Header": {
                        "Status": 200,
                        "From": clientAddress,
                        "Role": RolesModule.Roles.SPEAKER.value
                    },
                    "Body": {
                        "Message": clientMessage["Body"]["Message"]
                    }
                }
                # Convert the message to JSON string
                message = json.dumps(message)
                serverSocket.sendto(message.encode(), peer)

        # Protocol
        message = {
            "Header": {
                "Status": 200,
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
        serverSocket.sendto(message.encode(), clientAddress)
                
    # If message is from listener, reply to the listener
    elif clientMessage["Header"]["Role"] == RolesModule.Roles.LISTENER.value:
        
        if clientAddress not in listPeerListener:
            listPeerListener.append(clientAddress)
            print('New peer added: ', clientAddress)
        
        # Protocol
        message = {
            "Header": {
                "Status": 200,
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
        serverSocket.sendto(message.encode(), clientAddress)
