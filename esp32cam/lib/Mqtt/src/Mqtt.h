#ifndef MQTT
#define MQTT

#define DEGUB_ESP

// Connection timeout
#define CON_TIMEOUT 10*1000

//#define BUILTIN_LED 2

// Deep Sleep
#define TIME_TO_SLEEP (uint64_t) 10*60*1000*1000

#include <Arduino.h>

#include <WiFi.h>
#include <string>
#include <PubSubClient.h>

#include "esp_timer.h"
#include <base64.h>
//#include "rgb.h"

#ifdef DEGUB_ESP
  #define DBG(x) Serial.println(x)
#else 
  #define DBG(...)
#endif

class Mqtt 
{
    public:
        Mqtt(
            //LedRGB led,
            
            const char* wifi_ssid,
            const char* wifi_password,

            const char* mqtt_host,
            uint16_t port,
            const char* username,
            const char* password,
            const char* sub_topic_pic,
            const char* pub_topic_pic
        );

        void setup(void);
        void pub_topic(const uint8_t* pic_buf, size_t length);
        void teste_topic(void);

        bool getState();
        
        void reconnect(void);
        void deep_sleep(void);

    private:
        //LedRGB led;

        const char* wifi_ssid;
        const char* wifi_password;

        const char* mqtt_host;
        uint16_t port;
        const char* username;
        const char* password;
        const char* sub_topic_pic;
        const char* pub_topic_pic;

        void setup_wifi(const char* wifi_ssid, const char* wifi_password);
        void setup_mqtt(void);

        void pub_topic_write(const uint8_t* pic_buf, size_t length);
        void pub_topic_P(const uint8_t* pic_buf, size_t length);
        void pub_topic_encode64(const uint8_t* pic_buf, size_t length);

        //void callback(char* topic, byte* payload, unsigned int length);

};

#endif 