import java.io.*;
import java.net.*;
import java.util.*;

public class server {
    private static final int PORT = 22222;
    private ServerSocket serverSocket;
    private Socket[] clients = new Socket[2];
    private DataInputStream[] dis = new DataInputStream[2];
    private DataOutputStream[] dos = new DataOutputStream[2];
    private String[] board = new String[9]; // Tic-Tac-Toe board
    private boolean gameActive = true;
    private int currentPlayer = 0; // Player 1 starts

    public server() throws IOException {
        serverSocket = new ServerSocket(PORT);
        System.out.println("Server started. Waiting for players...");
        acceptClients();
    }

    private void acceptClients() throws IOException {
        for (int i = 0; i < 2; i++) {
            clients[i] = serverSocket.accept();
            dis[i] = new DataInputStream(clients[i].getInputStream());
            dos[i] = new DataOutputStream(clients[i].getOutputStream());
            System.out.println("Player " + (i + 1) + " connected.");
            dos[i].writeUTF("You are Player " + (i + 1));
        }
        startGame();
    }

    private void startGame() throws IOException {
        while (gameActive) {
            try {
                int move = dis[currentPlayer].readInt();
                if (isValidMove(move)) {
                    board[move] = currentPlayer == 0 ? "X" : "O";
                    sendBoardUpdate();
                    if (checkGameState(move)) {
                        gameActive = false;
                        sendGameOver();
                    } else {
                        switchPlayer();
                    }
                }
            } catch (IOException e) {
                System.out.println("Player " + (currentPlayer + 1) + " disconnected.");
                gameActive = false;
                sendGameOver();
            }
        }
        closeEverything();
    }

    private void switchPlayer() {
        currentPlayer = 1 - currentPlayer; // Switch between 0 and 1
    }

    private boolean isValidMove(int move) {
        return (move >= 0 && move < 9 && board[move] == null);
    }

    private void sendBoardUpdate() throws IOException {
        for (int i = 0; i < 2; i++) {
            dos[i].writeUTF(Arrays.toString(board));
            dos[i].flush();
        }
    }

    private boolean checkGameState(int move) {
        // Check win conditions based on the last move
        int row = move / 3;
        int col = move % 3;

        // Check row, column, and diagonals
        String symbol = board[move];
        boolean rowWin = true, colWin = true;
        boolean diag1Win = true, diag2Win = true;
        
        for (int i = 0; i < 3; i++) {
            if (!symbol.equals(board[row * 3 + i]))
                rowWin = false;
            if (!symbol.equals(board[i * 3 + col]))
                colWin = false;
            if (!symbol.equals(board[i * 3 + i]))
                diag1Win = false;
            if (!symbol.equals(board[i * 3 + (2 - i)]))
                diag2Win = false;
        }

        boolean won = rowWin || colWin || (move % 4 == 0 && diag1Win) || (move % 2 == 0 && move != 4 && diag2Win);
        if (won) {
            for (int i = 0; i < 2; i++) {
                try {
                    dos[i].writeUTF("Player " + (currentPlayer + 1) + " wins!");
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        return won || Arrays.stream(board).allMatch(Objects::nonNull); // Check if all cells are filled
    }

    private void sendGameOver() throws IOException {
        for (int i = 0; i < 2; i++) {
            if (clients[i] != null && !clients[i].isClosed()) {
                dos[i].writeUTF("Game Over");
                dos[i].flush();
            }
        }
    }

    private void closeEverything() {
        try {
            for (int i = 0; i < 2; i++) {
                if (clients[i] != null) clients[i].close();
                if (dis[i] != null) dis[i].close();
                if (dos[i] != null) dos[i].close();
            }
            if (serverSocket != null) serverSocket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        try {
            new TicTacToeServer();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
