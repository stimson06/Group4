#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid     = "********";//add your wifi username and password
const char* password = "********";

// All left-side pins
#define LED_LEFT     13
#define LED_RIGHT    12
#define LED_FORWARD  14
#define LED_BACKWARD 27

WiFiUDP udp;
const int PORT = 5005;
char packet[32];

void allOff() {
    digitalWrite(LED_LEFT,     LOW);
    digitalWrite(LED_RIGHT,    LOW);
    digitalWrite(LED_FORWARD,  LOW);
    digitalWrite(LED_BACKWARD, LOW);
}

void setup() {
    Serial.begin(115200);

    pinMode(LED_LEFT,     OUTPUT);
    pinMode(LED_RIGHT,    OUTPUT);
    pinMode(LED_FORWARD,  OUTPUT);
    pinMode(LED_BACKWARD, OUTPUT);
    allOff();

    // Startup test — flash each LED so you know wiring works
    Serial.println("Testing LEDs...");
    digitalWrite(LED_LEFT,     HIGH); delay(400); digitalWrite(LED_LEFT,     LOW);
    digitalWrite(LED_RIGHT,    HIGH); delay(400); digitalWrite(LED_RIGHT,    LOW);
    digitalWrite(LED_FORWARD,  HIGH); delay(400); digitalWrite(LED_FORWARD,  LOW);
    digitalWrite(LED_BACKWARD, HIGH); delay(400); digitalWrite(LED_BACKWARD, LOW);

    // Connect WiFi
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(300);
        Serial.print(".");
    }
    Serial.println();
    Serial.println("Connected! ESP32 IP: " + WiFi.localIP().toString());
    Serial.println("Copy this IP into your OpenMV script");

    udp.begin(PORT);
    Serial.println("Listening on port " + String(PORT) + " ...");
}

void loop() {
    int len = udp.parsePacket();
    if (len > 0) {
        udp.read(packet, sizeof(packet) - 1);
        packet[len] = '\0';
        String gesture = String(packet);
        gesture.trim();
        Serial.println("Received: " + gesture);

        allOff();
        if      (gesture == "left")     digitalWrite(LED_LEFT,     HIGH);
        else if (gesture == "right")    digitalWrite(LED_RIGHT,    HIGH);
        else if (gesture == "forward")  digitalWrite(LED_FORWARD,  HIGH);
        else if (gesture == "backward") digitalWrite(LED_BACKWARD, HIGH);
    }
}