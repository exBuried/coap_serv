#include <stdbool.h>
#include <string.h>
#include "coap.h"
#include "Arduino.h"
#include <DHT.h>


static char light = '0';

const uint16_t rsplen = 1500;
static char rsp[1500] = "";
void build_rsp(void);

// humidité et température
#define DHTTYPE DHT22
#define DHTPIN A0

DHT dht(DHTPIN, DHTTYPE);

// luminosité
#define lightPin A3
int lightLevel;



static int led = 6;
void endpoint_setup(void)
{                
    pinMode(led, OUTPUT);     
    build_rsp();
}

static const coap_endpoint_path_t path_well_known_core = {2, {".well-known", "core"}};
static int handle_get_well_known_core(coap_rw_buffer_t *scratch, const coap_packet_t *inpkt, coap_packet_t *outpkt, uint8_t id_hi, uint8_t id_lo)
{
    return coap_make_response(scratch, outpkt, (const uint8_t *)rsp, strlen(rsp), id_hi, id_lo, &inpkt->tok, COAP_RSPCODE_CONTENT, COAP_CONTENTTYPE_APPLICATION_LINKFORMAT);
}

static const coap_endpoint_path_t path_temp = {1, {"temperature"}};
 
static int handle_get_temp(coap_rw_buffer_t *scratch, const coap_packet_t *inpkt,coap_packet_t *outpkt,uint8_t id_hi, uint8_t id_lo)
{
    char response[16];
    dtostrf(dht.readTemperature(), 5, 2, response);
    return coap_make_response(scratch,outpkt,(const uint8_t *)&response,strlen(response),id_hi,id_lo,&inpkt->tok,COAP_RSPCODE_CONTENT,COAP_CONTENTTYPE_TEXT_PLAIN);
}

static const coap_endpoint_path_t path_lum = {1, {"light"}};
 
static int handle_get_light(coap_rw_buffer_t *scratch, const coap_packet_t *inpkt, coap_packet_t *outpkt,uint8_t id_hi, uint8_t id_lo)
{
    char response[16];
 
    dtostrf(analogRead(lightPin), 5, 2, response);
    return coap_make_response(scratch, outpkt,(const uint8_t *)&response,strlen(response),id_hi,id_lo,&inpkt->tok,COAP_RSPCODE_CONTENT,COAP_CONTENTTYPE_TEXT_PLAIN);
}

static const coap_endpoint_path_t path_humi = {1, {"humidite"}};
 
static int handle_get_humi(coap_rw_buffer_t *scratch,const coap_packet_t *inpkt,coap_packet_t *outpkt,uint8_t id_hi,uint8_t id_lo)
{
    char response[16];
 
    dtostrf(dht.readHumidity(), 5, 2, response);
    return coap_make_response(scratch,outpkt,(const uint8_t *)&response,strlen(response),id_hi,id_lo,&inpkt->tok,COAP_RSPCODE_CONTENT,COAP_CONTENTTYPE_TEXT_PLAIN);
}

extern const coap_endpoint_t endpoints[] =
{
    {COAP_METHOD_GET, handle_get_well_known_core, &path_well_known_core, "ct=40"},
	  {COAP_METHOD_GET, handle_get_temp, &path_temp, "ct=0"},
    {COAP_METHOD_GET, handle_get_humi, &path_humi, "ct=0"},
    {COAP_METHOD_GET, handle_get_light, &path_lum, "ct=0"},
    {(coap_method_t)0, NULL, NULL, NULL}
};

void build_rsp(void)
{
    uint16_t len = rsplen;
    const coap_endpoint_t *ep = endpoints;
    int i;

    len--; // Null-terminated string

    while(NULL != ep->handler)
    {
        if (NULL == ep->core_attr) {
            ep++;
            continue;
        }

        if (0 < strlen(rsp)) {
            strncat(rsp, ",", len);
            len--;
        }

        strncat(rsp, "<", len);
        len--;

        for (i = 0; i < ep->path->count; i++) {
            strncat(rsp, "/", len);
            len--;

            strncat(rsp, ep->path->elems[i], len);
            len -= strlen(ep->path->elems[i]);
        }

        strncat(rsp, ">;", len);
        len -= 2;

        strncat(rsp, ep->core_attr, len);
        len -= strlen(ep->core_attr);

        ep++;
    }
}

