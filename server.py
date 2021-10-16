import socket
import threading
import time

HEADER = 64
PORT = 3306
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "ISO-8859-1"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
   print(f"[NEW CONNECTIONS] {addr} connected.")

   connected = True
   while connected:
      msg_length = conn.recv(HEADER).decode(FORMAT)
      print(msg_length)

      if msg_length:
         msg_length = int(msg_length)
         msg = conn.recv(msg_length).decode(FORMAT)
         print(msg)

         if msg == DISCONNECT_MESSAGE:
            connected = False

         print(f"[{addr}] {msg}")

         conn.send("Msg received".encode(FORMAT))
   
   conn.close()


def start():
   server.listen()
   print(f"[LISTENING] server is listening on {SERVER}")
   # time.sleep(3)
   # conn, addr = server.accept()
   # time.sleep(3)

   #handle_client(conn, addr)


   while True:
      conn, addr = server.accept()
      # create new thread to handle client
      thread = threading.Thread(target=handle_client, args=(conn, addr))
      thread.start()

      handle_client(conn, addr)

      # prints the number of threads running in this process = number of clients
      print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()

