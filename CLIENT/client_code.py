import socket 

def run_client():

    server_ip = '172.25.229.18'
    server_port = 9000
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((server_ip, server_port))

    print(f"Connected to server at {server_ip}:{server_port}")

    while True:

        message = input("Enter message to send to server (type 'close' to exit): ")
        client.send(message.encode('utf-8')[:1024])

        # NOW WE RECIEVE MESSAGE FROM THE SERVER 
        response = client.recv(1024).decode('utf-8') 

        # if the server send me a closed message then i should close the connection
        if response.lower() == 'closed':
            print("Server has closed the connection.")
            break

        print("response from server:", {response})

    # now we close the clien socket 
    client.close()
    print("Client socket closed.")

run_client()