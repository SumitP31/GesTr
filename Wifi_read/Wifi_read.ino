#include <WiFiNINA.h>

char ssid[] = "Arduino_AP";
char pass[] = "12345678";

WiFiServer server(8080);

void setup() {
  Serial.begin(115200);
  while (!Serial);

  Serial.println("Starting AP...");

  // Start Access Point
  if (WiFi.beginAP(ssid, pass) != WL_AP_LISTENING) {
    Serial.println("AP start failed");
    while (1);
  }

  WiFi.lowPowerMode();  // Keep AP running
  delay(2000);

  Serial.print("AP IP: ");
  Serial.println(WiFi.localIP());

  server.begin();
  Serial.println("TCP Server started (port 8080)");
}

void loop() {
  WiFiClient client = server.available();
  // int client = 1;
  if (1) {
    Serial.println("Client connected!");

    // while (client.connected()) {
      client.println("Hello from Arduino!");
      delay(200);
    // }

    client.stop();
    Serial.println("Client disconnected");
  }
}
