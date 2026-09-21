import socket
import sys

# Get the listening port from the command line.
port = int(sys.argv[1])

# Create a TCP socket.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow the program to reuse the port after restarting.
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Listen for connections on the specified port.
server.bind(("0.0.0.0", port))
server.listen()

print(f"Chat server is listening on port {port}")

# Wait for another computer to connect.
while True:
    connection, address = server.accept()

    print(f"Connected to {address}")

    # Receive a message.
    message = connection.recv(1024).decode("utf-8")

    print(f"Message received: {message}")

    connection.close()