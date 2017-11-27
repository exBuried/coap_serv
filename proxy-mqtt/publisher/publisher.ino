#include <DHT_U.h>
#include <DHT.h>

#include <PubSubClient.h>
#include <WiFi.h>

#define DELAY 5000

// humidité et température
#define DHTTYPE DHT22
#define DHTPIN A0
DHT dht(DHTPIN, DHTTYPE);

// luminosité
#define lightPin A3
int lightLevel;

#define mqtt_port 1883
#define MQTT_Broker "192.168.1.59"

char ssid[] = "Freeboite";      // your network SSID (name)
char pass[] = "(&hkazer!8g";   // your network password
int keyIndex = 0;                // your network key Index number (needed only for WEP)
IPAddress ip(192, 168, 1, 50);

int status = WL_IDLE_STATUS;
WiFiClient client;

void printWifiStatus() {
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
}

PubSubClient mqtt_client(client);



void setup() {
  //Connexion au WiFi :
  Serial.begin(9600);
  while(!Serial){ }

  WiFi.config(ip);

  if (WiFi.begin(ssid, pass)==0){
    Serial.println("Failed to Configure WiFi");
    while(1);
  }
  Serial.println();
  printWifiStatus();

  //Connexion au broker mqtt
  mqtt_client.setServer(MQTT_Broker, 1883);
  
}

void reconnect() {
 // Loop until we're reconnected
 while (!mqtt_client.connected()) {
 Serial.print("Attempting MQTT connection...");
 // Attempt to connect
 
 if (mqtt_client.connect("RaspDuino")) {
  Serial.println("connected");
  // ... and subscribe to topic

  mqtt_client.subscribe("sensor");
  mqtt_client.subscribe("sensor/temperature");
  mqtt_client.subscribe("sensor/humidite");
  mqtt_client.subscribe("sensor/luminosite");
  
 } else {
  Serial.print("failed, rc=");
  Serial.print(mqtt_client.state());
  Serial.println(" try again in 5 seconds");
  // Wait 5 seconds before retrying
  delay(5000);
  }
 }
}

void loop() {

  if(!mqtt_client.connected()){
    reconnect();
  }

  char buf[10];
  dtostrf(dht.readTemperature(), 5, 2, buf);
  mqtt_client.publish("sensor/temperature", buf, true);
  //mqtt_client.publish("sensor", strcat("Temperature  ", buf));
  
  dtostrf(dht.readHumidity(), 5, 2, buf);
  mqtt_client.publish("sensor/humidite", buf, true);
  //mqtt_client.publish("sensor", strcat("Humidite  ", buf));
  
  sprintf(buf, "%d", analogRead(lightPin));
  mqtt_client.publish("sensor/luminosite", buf, true);
  //mqtt_client.publish("sensor", strcat("Luminosite  ", buf));

  delay(DELAY);
  
  
  // put your main code here, to run repeatedly:

}
