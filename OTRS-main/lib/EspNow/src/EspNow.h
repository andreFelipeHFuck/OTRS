#ifndef ESP_NOW
#define ESP_NOW

#include <Arduino.h>
#include <WiFi.h>

#include "esp_now.h"

void mac_address();

class EspNowSend{
    private:
        EspNowSend(
            uint8_t mac_address[6]
        );

        void setup();
        esp_err_t send_mensage();


    public:
        uint8_t broadcast_address[6];
};

class EspNowReceptor{

};


#endif ESP_NOW