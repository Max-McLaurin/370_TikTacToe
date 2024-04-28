import socket

def main():
    host = '10.0.0.224'  # Server IP
    port = 65435         # Server port

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print("Connected to server at {}:{}".format(host, port))

        while True:
            # Receive game board or game updates
            server_response = client_socket.recv(4096).decode('utf-8')
            if not server_response:
                break  # Server has closed the connection
            
            print(server_response)  # Print the game board and whose turn it is

            if "It's Player" in server_response and f"It's Player {server_response[-1]}" not in server_response:
                continue  # If it's not this client's turn, skip sending a move.

            # Prompt for a move
            move = input("Enter your move (row col): ")
            if move.lower() == 'exit':
                break
            client_socket.send(move.encode('utf-8'))

    except Exception as e:
        print("Unable to connect to the server or an error occurred:", e)
    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
