import socket
import threading
import random

SERVERHOST = '127.0.0.1'
SERVERPORT = 8080

clients=[]
waiting=[]

def findRandomAndSend(server,address):
    random_client = random.choice(waiting)
    while random_client == address:
        random_client = random.choice(waiting)
    random_client_str = str(random_client).encode('utf-8')
    server.sendto(random_client_str,address)
    server.sendto(str(address).encode('utf-8'),random_client)
    waiting.remove(address)
    waiting.remove(random_client)

def createServer():
    try:
        server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        server.bind((SERVERHOST,SERVERPORT))
        print(f"Server running on {SERVERHOST} : {SERVERPORT}")
        return server
    except:
        print("Something Went Wrong")

server = createServer()

while True:
    dataRecevied, address = server.recvfrom(2048)
    if address not in clients:
        clients.append(address)
    dataRecevied = dataRecevied.decode('utf-8')
    if dataRecevied == "!connect":
        waiting.append(address)
        find_random_send_thread = threading.Thread(target=findRandomAndSend,args=(server,address))
        find_random_send_thread.start()
    elif dataRecevied == "!exit":
        clients.remove(address)
    print(f"List of Clients connected: {clients}")
    print(f"List of waiting connected: {waiting}")
    

