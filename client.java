import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.*;
import java.util.Arrays;

public class TicTacToeClient extends JFrame implements Runnable {
    private static final int PORT = 22222;
    private static final String SERVER_IP = "10.205.7.170"; // Change to your server IP
    private Socket socket;
    private DataOutputStream dos;
    private DataInputStream dis;

    private JButton[] buttons = new JButton[9];
    private JLabel messageLabel = new JLabel("Connecting to server...");

    public TicTacToeClient() {
        super("Tic-Tac-Toe Client");
        setLayout(new GridLayout(3, 3));
        setSize(300, 300);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        initializeBoard();
        setVisible(true);

        connectToServer();
        new Thread(this).start();
    }

    private void initializeBoard() {
        for (int i = 0; i < 9; i++) {
            JButton button = new JButton();
            button.setFont(new Font("Arial", Font.BOLD, 40));
            button.setFocusPainted(false);
            button.addActionListener(e -> {
                if (((JButton) e.getSource()).getText().equals("") && !messageLabel.getText().contains("Your turn")) {
                    int index = Arrays.asList(buttons).indexOf(e.getSource());
                    try {
                        dos.writeInt(index);
                        dos.flush();
                    } catch (IOException ex) {
                        ex.printStackTrace();
                    }
                }
            });
            buttons[i] = button;
            add(button);
        }
        add(messageLabel, BorderLayout.SOUTH);
    }

    private void connectToServer() {
        try {
            socket = new Socket(SERVER_IP, PORT);
            dos = new DataOutputStream(socket.getOutputStream());
            dis = new DataInputStream(socket.getInputStream());
            messageLabel.setText("Connected to server");
        } catch (IOException e) {
            messageLabel.setText("Unable to connect to server");
            e.printStackTrace();
        }
    }

    @Override
    public void run() {
        try {
            while (true) {
                String serverMessage = dis.readUTF();
                if (serverMessage.contains("You are Player")) {
                    SwingUtilities.invokeLater(() -> messageLabel.setText(serverMessage));
                } else if (serverMessage.startsWith("[") && serverMessage.endsWith("]")) {
                    updateBoard(serverMessage);
                } else if (serverMessage.contains("wins") || serverMessage.contains("Game Over")) {
                    SwingUtilities.invokeLater(() -> {
                        messageLabel.setText(serverMessage);
                        for (JButton button : buttons) {
                            button.setEnabled(false);
                        }
                    });
                    break;
                }
            }
        } catch (IOException e) {
            messageLabel.setText("Lost connection to server");
            e.printStackTrace();
        }
    }

    private void updateBoard(String serverMessage) {
        String[] board = serverMessage.replaceAll("\\[|\\]", "").split(", ");
        SwingUtilities.invokeLater(() -> {
            for (int i = 0; i < board.length; i++) {
                buttons[i].setText(board[i].trim().isEmpty() ? "" : board[i].trim());
            }
        });
    }

    public static void main(String[] args) {
        new TicTacToeClient();
    }
}
