package pac;

import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

public class MainApplication extends JFrame {
    private JTextArea promptTextArea;
    private JTextArea responseTextArea;
    private JButton generateButton;
    private JButton selectComponentsButton;
    private JButton selectWorkflowButton;
    private JButton savePromptButton;
    private JLabel statusLabel;
    private HttpClient httpClient;
    private JFileChooser fileChooser;

    private static final String BACKEND_URL = "http://localhost:5000";
    private static final String BASE_DIR = "C:\\Users\\elmou\\.spyder-py3\\AutoM_AI";
    private static final String PROMPTS_DIR = BASE_DIR + "\\prompts";
    private static final String RESPONSES_DIR = BASE_DIR + "\\responses";
    private static final String XML_DIR = BASE_DIR + "\\xml_files";
    private static final String INPUT_XML_DIR = BASE_DIR + "\\input_xml"; // New directory for selected XML components
    private static final String MAIN_PY_PATH = BASE_DIR + "\\main.py";
    private static final String PROMPT_INITIAL_PATH = BASE_DIR + "\\prompt_initial.txt";

    public MainApplication() {
        initializeComponents();
        setupLayout();
        setupEventListeners();
        createDirectories();
        setupFileChooser();
        httpClient = HttpClient.newHttpClient();
    }

    private void initializeComponents() {
        setTitle("WORKS PLATFORM - Générateur d'Interface UI");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(1200, 800);
        setLocationRelativeTo(null);

        Color primaryBlue = new Color(52, 73, 153);
        Color secondaryBlue = new Color(78, 147, 195);
        Color lightBlue = new Color(135, 206, 235);
        Color greenColor = new Color(40, 167, 69);
        Color orangeColor = new Color(255, 140, 0);
        Color backgroundColor = new Color(248, 249, 250);
        Color textColor = new Color(33, 37, 41);

        getContentPane().setBackground(backgroundColor);

        promptTextArea = new JTextArea(10, 50);
        promptTextArea.setLineWrap(true);
        promptTextArea.setWrapStyleWord(true);
        promptTextArea.setFont(new Font("Segoe UI", Font.PLAIN, 14));
        promptTextArea.setBackground(Color.WHITE);
        promptTextArea.setForeground(textColor);
        promptTextArea.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createTitledBorder(
                        BorderFactory.createLineBorder(primaryBlue, 2),
                        "✨ Entrez votre prompt ici :",
                        0, 0, new Font("Segoe UI", Font.BOLD, 14), primaryBlue
                ),
                BorderFactory.createEmptyBorder(10, 10, 10, 10)
        ));

        responseTextArea = new JTextArea(18, 50);
        responseTextArea.setLineWrap(true);
        responseTextArea.setWrapStyleWord(true);
        responseTextArea.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        responseTextArea.setEditable(false);
        responseTextArea.setBackground(Color.WHITE);
        responseTextArea.setForeground(textColor);
        responseTextArea.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createTitledBorder(
                        BorderFactory.createLineBorder(secondaryBlue, 2),
                        "📋 Réponse du système :",
                        0, 0, new Font("Segoe UI", Font.BOLD, 14), secondaryBlue
                ),
                BorderFactory.createEmptyBorder(10, 10, 10, 10)
        ));

        generateButton = new JButton("🚀 Générer Interface");
        selectComponentsButton = new JButton("📦 Select Components");
        selectWorkflowButton = new JButton("⚡ Select Workflow");
        savePromptButton = new JButton("💾 Sauvegarder Prompt");

        styleButton(generateButton, primaryBlue, textColor);
        styleButton(selectComponentsButton, orangeColor, textColor);
        styleButton(selectWorkflowButton, lightBlue, textColor);
        styleButton(savePromptButton, greenColor, textColor);

        statusLabel = new JLabel("🟢 Système prêt - WORKS PLATFORM");
        statusLabel.setForeground(primaryBlue);
        statusLabel.setFont(new Font("Segoe UI", Font.BOLD, 12));

        addHoverEffect(generateButton, primaryBlue);
        addHoverEffect(selectComponentsButton, orangeColor);
        addHoverEffect(selectWorkflowButton, lightBlue);
        addHoverEffect(savePromptButton, greenColor);
    }

    private void styleButton(JButton button, Color bg, Color fg) {
        button.setPreferredSize(new Dimension(180, 45));
        button.setBackground(bg);
        button.setForeground(fg);
        button.setFont(new Font("Segoe UI", Font.BOLD, 12));
        button.setFocusPainted(false);
    }

    private void setupLayout() {
        setLayout(new BorderLayout());
        Color backgroundColor = new Color(248, 249, 250);
        Color primaryBlue = new Color(52, 73, 153);

        JPanel headerPanel = new JPanel(new BorderLayout());
        headerPanel.setBackground(primaryBlue);
        headerPanel.setBorder(BorderFactory.createEmptyBorder(15, 20, 15, 20));

        JLabel titleLabel = new JLabel("WORKS PLATFORM", SwingConstants.CENTER);
        titleLabel.setFont(new Font("Segoe UI", Font.BOLD, 24));
        titleLabel.setForeground(Color.WHITE);

        JLabel subtitleLabel = new JLabel("Générateur d'Interface UI - Intelligence Artificielle", SwingConstants.CENTER);
        subtitleLabel.setFont(new Font("Segoe UI", Font.PLAIN, 14));
        subtitleLabel.setForeground(new Color(200, 220, 255));

        JPanel titlePanel = new JPanel(new BorderLayout());
        titlePanel.setBackground(primaryBlue);
        titlePanel.add(titleLabel, BorderLayout.CENTER);
        titlePanel.add(subtitleLabel, BorderLayout.SOUTH);

        headerPanel.add(titlePanel, BorderLayout.CENTER);

        JPanel mainPanel = new JPanel(new BorderLayout());
        mainPanel.setBackground(backgroundColor);
        mainPanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        JPanel topPanel = new JPanel(new BorderLayout());
        topPanel.setBackground(backgroundColor);
        topPanel.setBorder(BorderFactory.createEmptyBorder(0, 0, 20, 0));
        topPanel.add(new JScrollPane(promptTextArea), BorderLayout.CENTER);

        // Panel pour les boutons avec deux rangées
        JPanel buttonPanel = new JPanel(new GridLayout(2, 2, 20, 10));
        buttonPanel.setBackground(backgroundColor);
        buttonPanel.setBorder(BorderFactory.createEmptyBorder(15, 50, 15, 50));
        
        buttonPanel.add(generateButton);
        buttonPanel.add(savePromptButton);
        buttonPanel.add(selectComponentsButton);
        buttonPanel.add(selectWorkflowButton);

        topPanel.add(buttonPanel, BorderLayout.SOUTH);

        JPanel bottomPanel = new JPanel(new BorderLayout());
        bottomPanel.setBackground(backgroundColor);
        bottomPanel.add(new JScrollPane(responseTextArea), BorderLayout.CENTER);

        JPanel statusPanel = new JPanel(new BorderLayout());
        statusPanel.setBackground(new Color(240, 242, 245));
        statusPanel.setBorder(BorderFactory.createEmptyBorder(10, 20, 10, 20));
        statusPanel.add(statusLabel, BorderLayout.WEST);

        JLabel timeLabel = new JLabel();
        timeLabel.setFont(new Font("Segoe UI", Font.PLAIN, 10));
        timeLabel.setForeground(new Color(100, 100, 100));
        statusPanel.add(timeLabel, BorderLayout.EAST);

        Timer timer = new Timer(1000, e -> {
            timeLabel.setText(LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss")));
        });
        timer.start();

        add(headerPanel, BorderLayout.NORTH);
        mainPanel.add(topPanel, BorderLayout.NORTH);
        mainPanel.add(bottomPanel, BorderLayout.CENTER);
        add(mainPanel, BorderLayout.CENTER);
        add(statusPanel, BorderLayout.SOUTH);
    }

    private void setupEventListeners() {
        generateButton.addActionListener(e -> generateInterface());
        selectComponentsButton.addActionListener(e -> selectComponents());
        selectWorkflowButton.addActionListener(e -> selectWorkflow());
        savePromptButton.addActionListener(e -> savePromptToFile());

        promptTextArea.getInputMap().put(KeyStroke.getKeyStroke("ctrl ENTER"), "generate");
        promptTextArea.getActionMap().put("generate", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                generateInterface();
            }
        });
    }

    private void setupFileChooser() {
        fileChooser = new JFileChooser();
        // Définir le répertoire de départ sur le répertoire AutoM_AI
        fileChooser.setCurrentDirectory(new File(BASE_DIR));
        
        // Filter pour les fichiers XML
        FileNameExtensionFilter xmlFilter = new FileNameExtensionFilter("Fichiers XML (*.xml)", "xml");
        fileChooser.addChoosableFileFilter(xmlFilter);
        
        // Filter pour les fichiers TXT
        FileNameExtensionFilter txtFilter = new FileNameExtensionFilter("Fichiers TXT (*.txt)", "txt");
        fileChooser.addChoosableFileFilter(txtFilter);
        
        fileChooser.setAcceptAllFileFilterUsed(true);
    }

    private void addHoverEffect(JButton button, Color originalColor) {
        Color hoverColor = originalColor.darker();
        button.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseEntered(MouseEvent e) {
                button.setBackground(hoverColor);
                button.setCursor(new Cursor(Cursor.HAND_CURSOR));
            }

            @Override
            public void mouseExited(MouseEvent e) {
                button.setBackground(originalColor);
                button.setCursor(new Cursor(Cursor.DEFAULT_CURSOR));
            }
        });
    }

    private void createDirectories() {
        try {
            // Créer le répertoire principal s'il n'existe pas
            Files.createDirectories(Paths.get(BASE_DIR));
            Files.createDirectories(Paths.get(PROMPTS_DIR));
            Files.createDirectories(Paths.get(RESPONSES_DIR));
            Files.createDirectories(Paths.get(XML_DIR));
            Files.createDirectories(Paths.get(INPUT_XML_DIR)); // Create input_xml directory
            
            // Afficher un message de confirmation
            setSuccessStatus("✅ Répertoires initialisés dans : " + BASE_DIR);
        } catch (IOException e) {
            showError("Erreur création répertoires : " + e.getMessage());
        }
    }

    private void selectComponents() {
        fileChooser.setDialogTitle("Sélectionner des fichiers (tous types)");
        fileChooser.setFileFilter(fileChooser.getAcceptAllFileFilter()); // Allow all files
        fileChooser.setMultiSelectionEnabled(true);

        int result = fileChooser.showOpenDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            File[] selectedFiles = fileChooser.getSelectedFiles();

            try {
                // Clear the input_xml directory first
                clearDirectory(INPUT_XML_DIR);

                int copiedCount = 0;
                StringBuilder copiedFiles = new StringBuilder();

                for (File file : selectedFiles) {
                    Path sourcePath = file.toPath();
                    Path targetPath = Paths.get(INPUT_XML_DIR, file.getName());

                    Files.copy(sourcePath, targetPath, StandardCopyOption.REPLACE_EXISTING);
                    copiedFiles.append("• ").append(file.getName()).append("\n");
                    copiedCount++;
                }

                if (copiedCount > 0) {
                    String message = "✅ " + copiedCount + " fichier(s) copié(s) vers input_xml/";
                    setSuccessStatus(message);

                    displayFormattedResponse("📦 Fichiers sélectionnés et copiés :\n\n" + 
                                           copiedFiles.toString() + 
                                           "\nDestination : " + INPUT_XML_DIR);

                    // Show confirmation dialog
                    JOptionPane.showMessageDialog(this, 
                        "Fichiers copiés avec succès !\n\n" + 
                        "Fichiers copiés : " + copiedCount + "\n" +
                        "Destination : " + INPUT_XML_DIR, 
                        "Sélection des fichiers", 
                        JOptionPane.INFORMATION_MESSAGE);
                } else {
                    showError("Aucun fichier sélectionné.");
                    setErrorStatus("❌ Aucun fichier sélectionné.");
                }

            } catch (IOException e) {
                showError("Erreur lors de la copie des fichiers : " + e.getMessage());
                setErrorStatus("❌ Échec de la copie des fichiers.");
            }
        }

        fileChooser.setMultiSelectionEnabled(false); // Reset to single selection
    }


    private void selectWorkflow() {
        fileChooser.setDialogTitle("Sélectionner un fichier Workflow (.txt)");
        fileChooser.setFileFilter(new FileNameExtensionFilter("Fichiers TXT (*.txt)", "txt"));
        
        int result = fileChooser.showOpenDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fileChooser.getSelectedFile();
            
            if (!selectedFile.getName().toLowerCase().endsWith(".txt")) {
                showError("Veuillez sélectionner un fichier .txt");
                setErrorStatus("❌ Format de fichier invalide.");
                return;
            }
            
            try {
                Path sourcePath = selectedFile.toPath();
                Path targetPath = Paths.get(BASE_DIR, selectedFile.getName());
                
                Files.copy(sourcePath, targetPath, StandardCopyOption.REPLACE_EXISTING);
                
                String content = Files.readString(sourcePath);
                displayFormattedResponse("⚡ Fichier Workflow sélectionné et copié :\n\n" + 
                                       "Fichier : " + selectedFile.getName() + "\n" +
                                       "Destination : " + BASE_DIR + "\n\n" +
                                       "Contenu :\n" + content);
                
                setSuccessStatus("✅ Workflow copié : " + selectedFile.getName());
                
                // Show confirmation dialog
                JOptionPane.showMessageDialog(this, 
                    "Workflow copié avec succès !\n\n" + 
                    "Fichier : " + selectedFile.getName() + "\n" +
                    "Destination : " + BASE_DIR, 
                    "Sélection du workflow", 
                    JOptionPane.INFORMATION_MESSAGE);
                
            } catch (IOException e) {
                showError("Erreur lors de la copie du fichier workflow : " + e.getMessage());
                setErrorStatus("❌ Échec de la copie du workflow.");
            }
        }
    }

    private void generateInterface() {
        String prompt = promptTextArea.getText().trim();
        if (prompt.isEmpty()) {
            showError("Veuillez entrer un prompt.");
            return;
        }
        
        setStatus("Envoi du prompt au serveur...");
        generateButton.setEnabled(false);

        // Run HTTP call async on Swing thread to avoid freezing UI
        SwingUtilities.invokeLater(() -> {
            try {
                String jsonBody = String.format("{\"prompt\": \"%s\"}",
                    prompt.replace("\"", "\\\"").replace("\n", "\\n"));
                
                HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(BACKEND_URL + "/generate"))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                    .build();

                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
                
                if (response.statusCode() == 200) {
                    displayFormattedResponse("🚀 Réponse du serveur :\n\n" + response.body());
                    setSuccessStatus("✅ Interface générée avec succès !");
                } else {
                    displayFormattedResponse("❌ Erreur serveur : " + response.body());
                    setErrorStatus("❌ Échec génération (code " + response.statusCode() + ")");
                }
            } catch (Exception e) {
                showError("Erreur lors de la requête : " + e.getMessage());
                setErrorStatus("❌ Erreur réseau");
            } finally {
                generateButton.setEnabled(true);
            }
        });
    }


    private void clearDirectory(String dirPath) throws IOException {
        Path directory = Paths.get(dirPath);
        if (Files.exists(directory)) {
            Files.walk(directory)
                 .filter(Files::isRegularFile)
                 .forEach(file -> {
                     try {
                         Files.delete(file);
                     } catch (IOException e) {
                         // Log error but continue
                         System.err.println("Could not delete file: " + file);
                     }
                 });
        }
    }

    private void savePromptToFile() {
        String prompt = promptTextArea.getText().trim();
        if (prompt.isEmpty()) {
            showError("Aucun prompt à sauvegarder.");
            return;
        }

        try {
            Files.writeString(Paths.get(PROMPT_INITIAL_PATH), prompt);
            setSuccessStatus("✅ Prompt sauvegardé : prompt_initial.txt");
            
            // Afficher une confirmation
            int option = JOptionPane.showConfirmDialog(this, 
                "Prompt sauvegardé avec succès !\n" + 
                "Fichier: prompt_initial.txt\n" +
                "Destination: " + BASE_DIR + "\n\n" +
                "Voulez-vous ouvrir le répertoire ?", 
                "Sauvegarde réussie", 
                JOptionPane.YES_NO_OPTION, 
                JOptionPane.INFORMATION_MESSAGE);
            
            if (option == JOptionPane.YES_OPTION) {
                try {
                    Desktop.getDesktop().open(new File(BASE_DIR));
                } catch (IOException ex) {
                    showError("Impossible d'ouvrir le répertoire : " + ex.getMessage());
                }
            }
            
        } catch (IOException e) {
            showError("Erreur lors de la sauvegarde : " + e.getMessage());
            setErrorStatus("❌ Échec de la sauvegarde.");
        }
    }

    private String sendToBackend(String prompt) throws Exception {
        String jsonBody = String.format("{\"prompt\": \"%s\"}",
                prompt.replace("\"", "\\\"").replace("\n", "\\n"));

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(BACKEND_URL + "/generate"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        if (response.statusCode() == 200) {
            return response.body();
        } else {
            throw new Exception("Erreur backend : " + response.statusCode());
        }
    }

    private void displayFormattedResponse(String response) {
        StringBuilder formatted = new StringBuilder();
        formatted.append("═══════════════════════════════════════════════\n");
        formatted.append("🎯 Résultat :\n\n").append(response).append("\n");
        formatted.append("═══════════════════════════════════════════════");
        responseTextArea.setText(formatted.toString());
        responseTextArea.setCaretPosition(0);
    }

    private void setStatus(String message) {
        SwingUtilities.invokeLater(() -> {
            statusLabel.setText("🔄 " + message);
            statusLabel.setForeground(new Color(52, 73, 153));
        });
    }

    private void setSuccessStatus(String message) {
        SwingUtilities.invokeLater(() -> {
            statusLabel.setText("✅ " + message);
            statusLabel.setForeground(new Color(40, 167, 69));
        });
    }

    private void setErrorStatus(String message) {
        SwingUtilities.invokeLater(() -> {
            statusLabel.setText("❌ " + message);
            statusLabel.setForeground(new Color(220, 53, 69));
        });
    }

    private void showError(String message) {
        JOptionPane.showMessageDialog(this, message, "Erreur", JOptionPane.ERROR_MESSAGE);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                try {
                    UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
                } catch (Exception e) {
                    // Fall back to default look and feel if system look and feel fails
                    System.err.println("Could not set system look and feel: " + e.getMessage());
                }
                MainApplication app = new MainApplication();
                app.setVisible(true);
            }
        });
    }
}