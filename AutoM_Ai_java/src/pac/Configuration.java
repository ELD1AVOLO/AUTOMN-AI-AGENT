package pac;

public class Configuration {
    public static final String BACKEND_HOST = "localhost";
    public static final int BACKEND_PORT = 5000;
    public static final String BACKEND_PROTOCOL = "http";

    public static String getBackendUrl() {
        return BACKEND_PROTOCOL + "://" + BACKEND_HOST + ":" + BACKEND_PORT;
    }
}
