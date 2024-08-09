from socket import *
import json
from utils import Roles as RolesModule
import threading

SERVER_PORT = 4000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', SERVER_PORT))
serverSocket.listen(5)
print('Welcome to Broadcast Server')

listPeerListener = []

def handle_client(connectionSocket, addr):
    global listPeerListener
    
    while True:
        clientMessage = connectionSocket.recv(2048)
        clientMessage = json.loads(clientMessage.decode())

        #SPEAKER
        if clientMessage["Header"]["Role"] == RolesModule.Roles.SPEAKER.value:
            print('Broadcasting to all listeners...')
            for peer in listPeerListener:
                message = {
                    "Header": {
                        "Status": 200,
                        "Phrase": "OK",
                        "From": addr,
                        "Role": RolesModule.Roles.SPEAKER.value
                    },
                    "Body": {
                        "Message": clientMessage["Body"]["Message"]
                    }
                }
                message = json.dumps(message)

                try:
                    peer.send(message.encode())
                    print(f'Message sent to {peer.getpeername()}')
                except Exception as e:
                    print(f"Error sending message to {peer.getpeername()}: {e}")

            message = {
                "Header": {
                    "Status": 200,
                    "Phrase": "OK",
                    "From": addr,
                    "Role": RolesModule.Roles.SERVER.value
                },
                "Body": {
                    "Message": "Broadcast Success"
                }
            }
            message = json.dumps(message)
            connectionSocket.send(message.encode())

        #LISTENER
        elif clientMessage["Header"]["Role"] == RolesModule.Roles.LISTENER.value:
            if connectionSocket not in listPeerListener:
                listPeerListener.append(connectionSocket)
                print(f'New listener added from {addr}')

            message = {
                "Header": {
                    "Status": 200,
                    "Phrase": "OK",
                    "From": addr,
                    "Role": RolesModule.Roles.SERVER.value
                },
                "Body": {
                    "Message": "Connection Success"
                }
            }
            message = json.dumps(message)
            connectionSocket.send(message.encode())  
            
while True:
    #Wait for connection
    connectionSocket, addr = serverSocket.accept()
    #Use Thread to handle concurrent (not waiting for the previous client to finish)
    client_handler = threading.Thread(target=handle_client, args=(connectionSocket, addr))
    client_handler.start()