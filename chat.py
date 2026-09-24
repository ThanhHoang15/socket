
import socket
import threading
import sys


# Create the TCP server

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(("0.0.0.0", port))

    server.listen()

    print(f"Server listening on port {port}")

    return server


# Server-side: Accept incoming connections and receive messages

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


# Client-side code

def connect_to_peer(ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((ip, port))

    print(f"Connected to {ip}:{port}")

    return client


# Section 3.3 - Question 1: Help command

def help_command():

    # Display all available commands and explain their functionality

    print("\nAvailable Commands:")

    # Display information about the help command
    print("help                         Display available commands")

    # Display information about the myip command
    print("myip                         Display the IP address of this computer")

    # Display information about the myport command
    print("myport                       Display the listening port of this program")

    # Display information about the connect command
    print("connect <destination> <port> Connect to another computer using its IP address and port")

    # Display information about the list command
    print("list                         Display all connected peers")

    # Display information about the terminate command
    print("terminate <connection id>    Terminate the specified connection")

    # Display information about the send command
    print("send <connection id> <message> Send a message to the specified peer (up to 100 characters)")

    # Display information about the exit command
    print("exit                         Close all connections and terminate the program")

    print()
    

# Section 3.3 - Question 2: Myip command

def myip_command():

    # Create a UDP socket to determine the computer's actual IP address
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Determine which local IP address would be used to reach this destination
        sock.connect(("8.8.8.8", 80))

        # Get the computer's IP address
        ip_address = sock.getsockname()[0]

        # Display the IP address
        print(f"IP Address: {ip_address}")

    except OSError:
        print("Error: Unable to determine the IP address.")

    finally:
        # Close the temporary socket
        sock.close()
 

# Section 3.3 - Question 3: Myport command

def myport_command(port):

    # Display the port on which this program is listening
    print(f"Listening Port: {port}")
 
 
# Combine the client and server into ONE program
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

        # Get a command from the user
        command = input(">> ").strip()

        # Display the available commands
        if command == "help":
            help_command()
            
        # Display the computer's IP address
        elif command == "myip":
            myip_command()    
        # Display the listening port
        elif command == "myport":
            myport_command(port)
        
        # Section 3.3 - Question 4: Connect command
        elif command.startswith("connect "):

            # Separate the command, IP address, and port
            parts = command.split()

            if len(parts) == 3:
                ip = parts[1]
                peer_port = int(parts[2])

                # Call the existing client function
                connect_to_peer(ip, peer_port)

            else:
                print("Error: Usage: connect <destination> <port>")        

        # Exit the program
        elif command == "exit":
            break

        # Handle empty input
        elif command == "":
            print("Error: Please enter a command.")
            

        # Handle invalid commands
        else:
            print("Error: Invalid command. Type 'help' to see available commands.")  
    server.close()


if __name__ == "__main__":
    main()
