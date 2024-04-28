import socket
import time

def main():
    host = '10.0.0.224'  # Server IP address
    port = 65437         # Server port

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Attempt to connect to the server
    attempts = 0
    while attempts < 5:
        try:
            client_socket.connect((host, port))
            print("Connected to server at {}:{}".format(host, port))
            break
        except socket.error as e:
            print("Connection attempt failed, trying again...")
            time.sleep(2)  # wait for 2 seconds before trying to reconnect
            attempts += 1
    else:
        print("Failed to connect to the server after several attempts.")
        return

    try:
        full_data = ''
        while True:
            # Receive game board or game updates
            data = client_socket.recv(4096).decode('utf-8')
            if not data:
                print("Server has closed the connection.")
                break  # Server has closed the connection or connection was lost

            full_data += data
            if '\n' in full_data:
                server_response, _, full_data = full_data.partition('\n')
                print(server_response)  # Display the game board and any messages

                # Determine if the received message contains a prompt for the player's move
                if "It's Player" in server_response and "turn" in server_response:
                    move = input("Enter your move (row col): ")
                    if move.lower() == 'exit':
                        break
                    client_socket.send(move.encode('utf-8'))
                elif "wins" in server_response or "draw" in server_response:
                    # If the game is over, break the loop
                    print(server_response)  # Display the final message
                    break

    except Exception as e:
        print("Unable to connect to the server or an error occurred:", e)
    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
