import socket
import threading

def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")

    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"[{client_address}] disconnected.")
                break

            print(f"[{client_address}] {message}")

            # Broadcast message to all clients
            for client in clients:
                if client != client_socket:
                    client.send(message.encode('utf-8'))

        except ConnectionError:  # Handle client disconnections gracefully
            print(f"[{client_address}] Connection error.")
            break

    # Close client connection
    client_socket.close()
    clients.remove(client_socket)

def start_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 5050))  # Replace with a different port if needed
        server_socket.listen(5)

        print("[SERVER] Server is listening on port 5050...")

        while True:
            client_socket, client_address = server_socket.accept()
            clients.append(client_socket)

            # Start a new thread to handle each client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

    except OSError as e:
        if e.errno == 10048:
            print("Port 5050 is already in use. Please choose a different port or stop the conflicting process.")
        else:
            raise

clients = []

# Start the server
start_server()
