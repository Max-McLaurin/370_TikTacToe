import socket
from _thread import start_new_thread

# Game state and player management
game_board = [[' ' for _ in range(3)] for _ in range(3)]
players = [None, None]  # Connections for player 1 and player 2
current_turn = 0

def client_thread(conn, player):
    global current_turn
    conn.send(str.encode("Welcome to Tic Tac Toe! You are Player " + str(player + 1)))
    
    while True:
        try:
            data = conn.recv(2048).decode('utf-8')
            if not data:
                print("Player {} disconnected".format(player + 1))
                break
            if player == current_turn:
                x, y = map(int, data.split())
                if game_board[x][y] == ' ':
                    game_board[x][y] = 'X' if player == 0 else 'O'
                    current_turn = 1 - current_turn  # Switch turns
                    send_game_board()
                else:
                    conn.send(str.encode("Invalid move"))
            else:
                conn.send(str.encode("Not your turn"))
        except Exception as e:
            print("Error handling data from player {}: {}".format(player + 1, e))
            break
    
    conn.close()

def send_game_board():
    board_visual = "\n".join([" | ".join(row) for row in game_board])
    for p in players:
        if p:
            p.sendall(str.encode(board_visual))

server_ip = '10.0.0.224'
port = 65433
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind((server_ip, port))
    server_socket.listen(2)
    print("Server started on {}:{}\nWaiting for connections...".format(server_ip, port))

    while True:
        conn, addr = server_socket.accept()
        print("Connected to:", addr)

        # Assign player 1 or 2
        player_index = 0 if players[0] is None else 1
        players[player_index] = conn
        start_new_thread(client_thread, (conn, player_index))

except socket.error as e:
    print("Socket error:", e)
except Exception as e:
    print("Error:", e)
finally:
    server_socket.close()
