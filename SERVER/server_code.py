import socket
import threading
from datetime import datetime

# This function handles each client individually
def handle_client(client_socket, addr):
    try:
        while True:
            # Receive the client's request
            request = client_socket.recv(1024).decode('utf-8')

            if not request:
                print(f"Client {addr} disconnected abruptly.")
                break

            # Check if the client wants to close the connection
            if request.lower() == 'close':
                client_socket.send("closed".encode('utf-8'))
                print(f"Connection with {addr} closed.")
                break

            # Print the request from the client and also the time it was received
            with open('server_log.txt', "a") as log: # here 'a' means append mode which will not overwrite the file
                log.write(f"{datetime.now()} - Received from {addr}: {request}\n")
                print(f"[{datetime.now()}] Received from {addr}: {request}")

            # Respond to the client
            response = "accepted"
            client_socket.send(response.encode('utf-8'))

    except Exception as e:
        with open('server_log.txt', "a") as log:
            log.write(f"{datetime.now()} - Error with {addr}: {e}\n")
        print(f" [{datetime.now()}]Error with {addr}: {e}")
    finally:
        client_socket.close()  # Close the client connection


# This function runs the main server logic
def run_Server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # THIS BASICALLY MEANS THAT the server itself is reachable at that IP and port,
    # and any client can connect to it
    server_ip = '172.25.229.18'
    server_port = 9000
    server.bind((server_ip, server_port))

    server.listen(5)  # Allow up to 5 pending connections
    with open('server_log.txt' , "a") as log:
        log.write(f"{datetime.now()} - Server started at {server_ip}:{server_port}\n")
        print(f" [{datetime.now()}]Server started at {server_ip}:{server_port}")

    try:
        while True:
            # accept incoming connection
            # When a client connects, server.accept() returns a new socket object (client_socket)
            # for that connection, and the address (client_address) of the connecting client.
            client_socket, client_address = server.accept()
            print(f"Connection established with {client_address}")

            # now i will make a thread for each client
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
            thread.start()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server.close()  # Close the server socket
        print("server is closed ")

run_Server()