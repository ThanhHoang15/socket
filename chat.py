
import socket
import threading
import sys

# Store all active peer connections
connections = []

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

        peer_ip = client_address[0]

        try:
            # Receive the other computer's listening port
            data = client_socket.recv(1024).decode()

            if not data.startswith("PORT:"):
                client_socket.close()
                continue

            peer_port = int(data.split(":")[1])

            # Reject duplicate connection
            duplicate = False

            for connection in connections:
                if connection["ip"] == peer_ip and connection["port"] == peer_port:
                    duplicate = True
                    break

            if duplicate:
                client_socket.sendall("DUPLICATE".encode())
                print("Error: Duplicate connection.")
                client_socket.close()
                continue

            # Reject connection if already connected to 3 peers
            if len(connections) >= 3:
                client_socket.sendall("FULL".encode())
                print("Error: Maximum of 3 connections allowed.")
                client_socket.close()
                continue

            # Tell the connecting computer the connection was accepted
            client_socket.sendall("OK".encode())

            # Store the incoming connection
            connections.append({
                "ip": peer_ip,
                "port": peer_port,
                "socket": client_socket
            })

            print(f"Connected to {peer_ip}:{peer_port}")

            thread = threading.Thread(
                target=handle_client,
                args=(client_socket,)
            )

            thread.start()

        except (ValueError, OSError):
            client_socket.close()

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
def connect_to_peer(ip, port, my_ip, my_port):

    # Section 3.3 - Question 4:
    # Reject self-connections
    if port == my_port and (ip == my_ip or ip == "127.0.0.1"):
        print("Error: Cannot connect to yourself.")
        return

    # Section 3.3 - Question 4:
    # Reject duplicate connections
    for connection in connections:
        if connection["ip"] == ip and connection["port"] == port:
            print("Error: Duplicate connection.")
            return
        
    # Allow maximum 3 peer connections
    if len(connections) >= 3:
        print("Error: Maximum of 3 connections allowed.")
        return

    # Create a TCP socket for the new connection
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Section 3.3 - Question 4:
        # Establish a new TCP connection to the specified IP address and port
        client.connect((ip, port))

        # Tell the other computer my listening port
        client.sendall(f"PORT:{my_port}".encode())

        # Section 3.3 - Question 4:
        # Wait for the other computer to accept or reject the connection
        response = client.recv(1024).decode()

        # Section 3.3 - Question 4:
        # Reject the connection if it is a duplicate
        if response == "DUPLICATE":
            print("Error: Duplicate connection.")
            client.close()
            return

        # Section 3.3 - Question 4:
        # Reject the connection if the peer already has 3 connections
        if response == "FULL":
            print("Error: The peer already has 3 connections.")
            client.close()
            return

        # Section 3.3 - Question 4:
        # Display a success message when the connection is established
        if response == "OK":
            print(f"Connected to {ip}:{port}")

            # Save the connection for duplicate checking
            connections.append({
                "ip": ip,
                "port": port,
                "socket": client
            })

    except socket.gaierror:
        # Section 3.3 - Question 4:
        # Reject an invalid IP address and display an error message
        print("Error: Invalid IP address.")

    except (ConnectionRefusedError, TimeoutError, OSError):
        # Section 3.3 - Question 4:
        # Display an error message if the connection fails
        print(f"Error: Could not connect to {ip}:{port}")


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
    
# Section 3.3 - Question 5: List command
def list_command():

    # Display the heading for the connection list
    print("id: IP address        Port No.")

    # Go through all active connections
    for i, connection in enumerate(connections, start=1):

        # Display the connection ID, peer IP address, and peer listening port
        print(f"{i}:  {connection['ip']}        {connection['port']}")   
    
 
 
# Combine the client and server into ONE program
def main():
    port = int(sys.argv[1])
    
    # Get this computer's IP address
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    my_ip = sock.getsockname()[0]
    sock.close()

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

                try:
                    peer_port = int(parts[2])
                except ValueError:
                    print("Error: Port must be a number.")
                    continue

                connect_to_peer(ip, peer_port, my_ip, port)

            else:
                print("Error: Usage: connect <destination> <port>")        

        # Exit the program
        elif command == "exit":
            break

        # Handle empty input
        elif command == "":
            print("Error: Please enter a command.")
        # Section 3.3 - Question 5: List command
        elif command == "list":

            # Display all active peer connections
            list_command()
            

        # Handle invalid commands
        else:
            print("Error: Invalid command. Type 'help' to see available commands.")  
    server.close()


if __name__ == "__main__":
    main()
