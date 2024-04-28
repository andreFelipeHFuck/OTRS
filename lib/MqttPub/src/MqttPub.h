#ifndef MQTT_PUB
#define MQTT_PUB

#define DEGUB_ESP

// Connection timeout
#define CON_TIMEOUT 10*1000

//#define BUILTIN_LED 2

// Deep Sleep
#define TIME_TO_SLEEP (uint64_t) 10*60*1000*1000

#include <Arduino.h>

#include <WiFi.h>
#include <PubSubClient.h>

#include "esp_timer.h"

#ifdef DEGUB_ESP
  #define DBG(x) Serial.println(x)
#else 
  #define DBG(...)
#endif

class MqttPub 
{
    public:
        MqttPub(
            const char* wifi_ssid,
            const char* wifi_password,

            const char* mqtt_host,
            uint16_t port,
            const char* username,
            const char* password,
            const char* topic_pic
        );

        void setup(void);
        void pub_topic(const uint8_t* pic_buf, size_t length);
        void pub_topic(const char* msg);
        void teste_topic(void);
        
        void reconnect(void);
        void deep_sleep(void);

    private:
        const char* wifi_ssid;
        const char* wifi_password;

        const char* mqtt_host;
        uint16_t port;
        const char* topic_pic;

        void setup_wifi( const char* wifi_ssid, const char* wifi_password);
        void setup_mqtt(void);

       // void callback(char* topic, byte* payload, unsigned int length);

};

#endif 