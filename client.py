import socket 

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

# creates client socket that uses SOCK_STREAM connection (TCP) and AF_INET (IPv4)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# attempts to connect to the given address
client.connect(ADDR)

def send(msg):
    # encodes the message in whatever format given
    message = msg.encode(FORMAT)
    msg_length = len(message)
    # encodes the length of the message and then sends it as a first message to the server
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)

    # sends the actual message to the server
    client.send(message)

    # prints the message sent by the server
    print(client.recv(2048).decode(FORMAT))

if __name__ ==  '__main__':
    print("[STARTING] server is starting...")

    while(True):
        msg = input('Escribe el mensaje: ')
        send(msg)


send(DISCONNECT_MESSAGE)