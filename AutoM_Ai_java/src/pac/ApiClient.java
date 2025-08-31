package pac;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class ApiClient {
    private final String backendUrl;

    public ApiClient(String backendUrl) {
        this.backendUrl = backendUrl;
    }

    public String sendPrompt(String prompt) {
        try {
            URL url = new URL(backendUrl + "/generate");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setDoOutput(true);

            String jsonInputString = "{\"prompt\": \"" + prompt.replace("\"", "\\\"") + "\"}";

            try (OutputStream os = conn.getOutputStream()) {
                byte[] input = jsonInputString.getBytes("utf-8");
                os.write(input, 0, input.length);
            }

            Scanner scanner = new Scanner(conn.getInputStream());
            String response = scanner.useDelimiter("\\A").next();
            scanner.close();

            return response;

        } catch (Exception e) {
            return "{\"error\": \"" + e.getMessage().replace("\"", "'") + "\"}";
        }
    }
}
