import socket
from _thread import start_new_thread

# Game state and player management
game_board = [[' ' for _ in range(3)] for _ in range(3)]
players = [None, None]  # Connections for player 1 and player 2
current_turn = 0

def check_win(board):
    # Check horizontal, vertical, and diagonal wins
    for line in range(3):
        if board[line][0] == board[line][1] == board[line][2] != ' ':  # Check rows
            return board[line][0]
        if board[0][line] == board[1][line] == board[2][line] != ' ':  # Check columns
            return board[0][line]
    if board[0][0] == board[1][1] == board[2][2] != ' ':  # Check diagonal
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':  # Check opposite diagonal
        return board[0][2]
    return None

def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def client_thread(conn, player):
    global current_turn
    symbols = ['X', 'O']
    player_symbol = symbols[player]
    
    welcome_message = "Welcome to Tic Tac Toe! You are Player " + str(player + 1) + f" ({player_symbol})"
    conn.send(str.encode(welcome_message))
    send_game_board_to_all()

    while True:
        try:
            data = conn.recv(2048).decode('utf-8')
            if not data:
                print("Player {} disconnected".format(player + 1))
                break
            
            if player == current_turn:
                x, y = map(int, data.split())
                if game_board[x][y] == ' ':
                    game_board[x][y] = player_symbol
                    if check_win(game_board):
                        send_game_board_to_all()
                        send_to_all(f"Player {player + 1} ({player_symbol}) wins!")
                        break
                    elif check_draw(game_board):
                        send_game_board_to_all()
                        send_to_all("Game is a draw!")
                        break
                    current_turn = 1 - current_turn
                    send_game_board_to_all()
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
    send_to_all(board_visual + "\nIt's Player {}'s turn ({}).".format(current_turn + 1, symbols[current_turn]))

def send_to_all(message):
    for p in players:
        if p:
            p.sendall(str.encode(message))

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

    wait_for_players(server_socket)

except socket.error as e:
    print("Socket error:", e)
except Exception as e:
    print("Error:", e)
finally:
    server_socket.close()
    print("Server has been closed.")
