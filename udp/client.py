from socket import *
from datetime import datetime
import socket as socketClient
import json
from utils import Roles as RolesModule

# Set up the socket
serverName = 'localhost'
serverPort = 4000
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Print the welcome message
print('Welcome to Broadcast Client')
role = int(input('Enter your role (1 = Listener, 2 = Speaker): '))

if RolesModule.Roles.LISTENER.value == role:
    print('You are a listener, please wait for the speaker')
    message = {
        "Header": {
            "From": socketClient.gethostbyname(socketClient.gethostname()),
            "Role": RolesModule.Roles.LISTENER.value
        },
        "Body": {
            "Message": None
        }
    }
    
    # Convert the message to JSON string
    message = json.dumps(message)
    
    # Send to the server
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    serverResponse, serverAddress = clientSocket.recvfrom(2048)
    
    # Decode the server response
    serverResponse = json.loads(serverResponse.decode())
    
    # Print the server response
    print('Server Response: ', serverResponse)
    print('From: ', serverResponse["Header"]["From"])
    print('Message: ', serverResponse["Body"]["Message"])
    
    # Receive the server response
    if(serverResponse["Header"]["Status"] == 200):
        # When Connected
        while True:
            serverResponse, serverAddress = clientSocket.recvfrom(2048)
            
            # Decode the server response
            serverResponse = json.loads(serverResponse.decode())
            if(serverResponse["Header"]["Status"] == 200):
                print('From: ', serverResponse["Header"]["From"])
                print('Message: ', serverResponse["Body"]["Message"])
    else:
        exit()
        
elif RolesModule.Roles.SPEAKER.value == role:
    print('You are a speaker')
    while True:
        messageBroadcast = input('Enter your message: ')
        
        # Break the loop if the message is empty
        if messageBroadcast == "":
            break
        
        # Change the message to the protocol format
        message = {
            "Header": {
                "From": socketClient.gethostbyname(socketClient.gethostname()),
                "Role": RolesModule.Roles.SPEAKER.value
            },
            "Body": {
                "Message": messageBroadcast,
            }
        }
        
        # Convert the message to JSON string
        message = json.dumps(message)

        # Send to the server
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        serverResponse, serverAddress = clientSocket.recvfrom(2048)
        
        # Decode the server response
        serverResponse = json.loads(serverResponse.decode())
        print('From: ', serverResponse["Header"]["From"])
        print('Message: ', serverResponse["Body"]["Message"])
        
else:
    print('Invalid role. Please try again')
    exit()

# Close the socket
clientSocket.close()
