import socket
import sys
import json

host = ''
port = 50000
backlog = 5
size = 1024

s = None
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind((host,port))
    myIP = socket.gethostbyname(socket.gethostname())
    print("Created socket at " + myIP + " on port " + str(port))
    print("Listening for client connections...")
    s.listen(backlog)
except socket.error as message:
    if s:
        s.close()
    print("Could not open socket: " + str(message))
    sys.exit(1)

client, address = s.accept()    # blocks until the pi connects
print("Accepted client connection from " + str(address[0]) + " on port " + str(address[1]))
while True:
    data = client.recv(size)
    #data = json.loads(data)
    #sensor = data["sensor"]
    print(data)