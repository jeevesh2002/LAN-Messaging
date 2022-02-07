import socket
import sys
import threading
import ast

SERVERHOST = '127.0.0.1'
SERVERPORT = 8080

ALIVE = True

# Handle Messages received
def handle(clientt):
    while ALIVE:
        try:
            data, address = clientt.recvfrom(2048)
            data = data.decode('utf-8')
            if data == "Sender Left The Chat":
                print(f"{address}:  {data}")
                clientt.close()
                del clientt
                break
            print(f"{address}:  {data}")
        except:
            pass
    main(SERVERHOST,SERVERPORT)


# Create client socket
clientCreated = False
def createClient():
    try:
        client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    except:
        print("Something went wrong in creating a socket")
    return client


# Connect to New client

def connectToNewClient(clientt):
    try:
        clientt.sendto("!connect".encode('utf-8'),(SERVERHOST,SERVERPORT))
        print("Connecting....")
        try:
            data , address = clientt.recvfrom(2048)
            data=data.decode('utf-8')
            print(data)
            return ast.literal_eval(data)
        except:
            pass
    except:
        pass


def main(SERVERHOST, SERVERPORT):
    try:
        client = createClient()
        recepient_address = connectToNewClient(client)
        print(recepient_address)

        handle_thread = threading.Thread(target=handle,args=(client,))
        handle_thread.start()


        while True:
            msg = input()
            if msg == "!exit":
                client.sendto(msg.encode('utf-8'),(SERVERHOST,SERVERPORT))
                client.sendto("Sender Left The Chat".encode('utf-8'),recepient_address)
                client.close()
                del client
                sys.exit()
                break
            elif msg=="!connect":
                recepient_address = connectToNewClient(client)
            else :
                try:
                    client.sendto(msg.encode('utf-8'),recepient_address)
                except:
                    print("Uh Uh Msg Not delivered try again")
    except:
        pass

main(SERVERHOST, SERVERPORT)
    
