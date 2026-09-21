import socket
import threading
import sys


#Create the TCP server

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(("0.0.0.0", port))

    server.listen()

    print(f"Server listening on port {port}")

    return server

#Server-side: Accept incoming connections and receive messages

def accept_connections(server):
    while True:
        client_socket, client_address = server.accept()

        print(f"Connected to {client_address}")

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket,)
        )

        thread.start()


def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)

            if not message:
                break

            print(message.decode())

        except OSError:
            break

    client_socket.close()
    
#Client-side code
    
def connect_to_peer(ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((ip, port))

    print(f"Connected to {ip}:{port}")

    return client



#Combine the client and server into ONE program

def main():
    port = int(sys.argv[1])

    server = start_server(port)

    server_thread = threading.Thread(
        target=accept_connections,
        args=(server,),
        daemon=True
    )

    server_thread.start()

    while True:
        command = input(">> ")

        if command == "exit":
            break

    server.close()

if __name__ == "__main__":
    main()