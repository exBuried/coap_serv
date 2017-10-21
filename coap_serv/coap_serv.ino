


#include <SPI.h>

#include <WiFi.h>
#include <stdint.h>
#include <WiFiUdp.h>
#include "coap.h"


char ssid[] = "WiFiDuino";      // your network SSID (name)
char pass[] = "tprliwifi";   // your network password
int keyIndex = 0;                // your network key Index number (needed only for WEP)
IPAddress ip(192, 168, 1, 50);



#define PORT 5683
/*  static uint8_t mac[] = {0x00, 0xAA, 0xBB, 0xCC, 0xDE, 0x02};*/
int status = WL_IDLE_STATUS;

WiFiServer server(80);

WiFiClient client;
WiFiUDP udp;
uint8_t packetbuf[256];
static uint8_t scratch_raw[32];
static coap_rw_buffer_t scratch_buf = {scratch_raw, sizeof(scratch_raw)};

void setup()
{
     int i;
    Serial.begin(9600);
    while (!Serial) 
    {
        ; // wait for serial port to connect. Needed for Leonardo only
    }
    WiFi.config(ip);

    if (WiFi.begin(ssid,pass) == 0)
    {
        Serial.println("Failed to configure WiFi");
        while(1);
    }
    Serial.println();
    udp.begin(PORT);

    printWifiStatus();
    coap_setup();
    endpoint_setup();
}

void printWifiStatus() {
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
}

void udp_send(const uint8_t *buf, int buflen)
{
  udp.beginPacket(udp.remoteIP(), udp.remotePort());
  while (buflen--)
    udp.write(*buf++);
  udp.endPacket();
}

void loop()
{
  int sz;
  int rc;
  coap_packet_t pkt;
  int i;


  if ((sz = udp.parsePacket()) > 0)
  {
    udp.read(packetbuf, sizeof(packetbuf));

    if (0 != (rc = coap_parse(&pkt, packetbuf, sz)))
    {
      Serial.print("Bad packet rc=");
      Serial.println(rc, DEC);
    }
    else
    {
      Serial.print("Get Request");
      Serial.println("");
      size_t rsplen = sizeof(packetbuf);
      coap_packet_t rsppkt;
      coap_handle_req(&scratch_buf, &pkt, &rsppkt);

      memset(packetbuf, 0, UDP_TX_PACKET_MAX_SIZE);
      if (0 != (rc = coap_build(packetbuf, &rsplen, &rsppkt)))
      {
        Serial.print("coap_build failed rc=");
        Serial.println(rc, DEC);
      }
      else
      {
        udp_send(packetbuf, rsplen);
      }
    }
  }
}

