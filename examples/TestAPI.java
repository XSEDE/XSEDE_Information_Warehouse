/* Test Information Services API
 */
//package TestAPI;

import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;

public class TestAPI
{
    public static String readFileFromUrl(String urlString) throws IOException {
        BufferedReader reader = null;
        StringBuffer buffer = new StringBuffer();
        try {
            URL url = new URL(urlString);
            reader = new BufferedReader(new InputStreamReader(url.openStream()));
            int read;
            char[] chars = new char[1024];
            while ((read = reader.read(chars)) != -1)
                            buffer.append(chars, 0, read);
        } catch (IOException e) {
            System.out.println("Error reading file from: " + urlString);
        } finally {
            if (reader != null)
                reader.close();
        }
        return buffer.toString();
    }

    public static void main(String[] args) {
        try {
            String URL = args[0];
            System.out.println("URL = " + URL);
            String Resp = readFileFromUrl(URL);
//            String Resp = readFileFromUrl("https://info.xsede.org/wh1/rdr-db/v1/rdr-xup/");
            System.out.println("Returned bytes = " + Resp.length());
            System.out.println("Leading 40 = " + Resp.substring(0,40) + " ..");
        } catch (IOException e) {
            System.out.println("Exception");
        }
    }
}
