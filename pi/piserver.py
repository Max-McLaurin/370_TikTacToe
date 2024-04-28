import socket
from _thread import start_new_thread

# Game state and player management
game_board = [[' ' for _ in range(3)] for _ in range(3)]
players = [None, None]  # Connections for player 1 and player 2
current_turn = 0

def client_thread(conn, player):
    global current_turn
    welcome_message = "Welcome to Tic Tac Toe! You are Player " + str(player + 1)
    conn.send(str.encode(welcome_message))
    send_game_board_to_all()  # Send initial game board to both players immediately

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
                    send_game_board_to_all()  # Send updated board to all players after a valid move
                else:
                    conn.send(str.encode("Invalid move. Try again."))
            else:
                conn.send(str.encode("It's not your turn. Please wait."))
        except Exception as e:
            print("Error handling data from player {}: {}".format(player + 1, e))
            break

    conn.close()

def send_game_board_to_all():
    board_visual = "\n".join([" | ".join(row) for row in game_board])
    for p in players:
        if p:
            p.sendall(str.encode(board_visual + "\nIt's Player {}'s turn.".format(current_turn + 1)))

def wait_for_players(server_socket):
    print("Waiting for players to connect...")
    player_count = 0
    while player_count < 2:
        conn, addr = server_socket.accept()
        print("Connected to:", addr)
        players[player_count] = conn
        player_count += 1

    for i in range(2):
        start_new_thread(client_thread, (players[i], i))

server_ip = '10.0.0.224'
port = 65434
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind((server_ip, port))
    server_socket.listen(2)
    print("Server started on {}:{}\n".format(server_ip, port))

    wait_for_players(server_socket)  # Wait for both players to connect and start their threads

except socket.error as e:
    print("Socket error:", e)
except Exception as e:
    print("Error:", e)
finally:
    server_socket.close()
    print("Server has been closed.")
