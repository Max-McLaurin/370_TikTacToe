import socket

def main():
    host = '10.0.0.224'  # Server IP
    port = 65434         # Server port

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print("Connected to server at {}:{}".format(host, port))

        while True:
            # Receive game board or game updates
            server_response = client_socket.recv(4096).decode('utf-8')
            if not server_response:
                print("Server has closed the connection.")
                break  # Server has closed the connection or connection was lost
            
            print(server_response)  # Display the game board and any messages

            # Determine if the received message contains a prompt for the player's move
            if "It's Player" in server_response and "turn" in server_response:
                move = input("Enter your move (row col): ")
                if move.lower() == 'exit':
                    break
                client_socket.send(move.encode('utf-8'))
            elif "wins" in server_response or "draw" in server_response:
                # If the game is over, break the loop
                break

    except Exception as e:
        print("Unable to connect to the server or an error occurred:", e)
    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
