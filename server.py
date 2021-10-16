import socket
import threading
import time

HEADER = 64
PORT = 3306
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# creates server socket that uses SOCK_STREAM connection (TCP) and AF_INET (IPv4)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binds the connection to the address that is going to be used to receive the connections
server.bind(ADDR)

def handle_client(conn, addr):
   print(f"[NEW CONNECTIONS] {addr} connected.")

   connected = True
   while connected:
      # receives the first message sent by the client which is the length of the real message
      msg_length = conn.recv(HEADER).decode(FORMAT)
      print(msg_length)

      if msg_length:
         msg_length = int(msg_length)
         # expects the message of the length given and receives it
         # server needs to know the length of the message that is about to be received
         msg = conn.recv(msg_length).decode(FORMAT)
         print(msg)

         if msg == DISCONNECT_MESSAGE:
            connected = False

         print(f"[{addr}] {msg}")

         # sends an acknowledgement of the message received back to the client
         conn.send("Msg received".encode(FORMAT))
   
   conn.close()


def start():
   # server waits for a connection request
   server.listen()
   print(f"[LISTENING] server is listening on {SERVER}")

   while True:
      conn, addr = server.accept()
      # create new thread to handle client
      thread = threading.Thread(target=handle_client, args=(conn, addr))
      thread.start()

      handle_client(conn, addr)

      # prints the number of threads running in this process = number of clients
      print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ ==  '__main__':
   print("[STARTING] server is starting...")
   start()

