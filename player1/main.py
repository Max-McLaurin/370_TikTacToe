import socket

def main():
    host = '10.0.0.224'  # Server IP
    port = 65433         # Server port

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except ConnectionError:
        print("Unable to connect to the server.")
        return

    print("Connected to server at {}:{}".format(host, port))
    server_message = client_socket.recv(1024).decode('utf-8')
    print(server_message)  # Welcome message

    try:
        while True:
            # Receive game board or game updates
            server_response = client_socket.recv(2048).decode('utf-8')
            if server_response:
                print(server_response)
            else:
                break  # Server has closed the connection

            # Send a move
            move = input("Enter your move (row col): ")
            if move.lower() == 'exit':
                break
            client_socket.send(move.encode('utf-8'))
    except Exception as e:
        print("An error occurred:", e)
    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
