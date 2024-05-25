#ifndef ESP_NOW
#define ESP_NOW

#include <Arduino.h>
#include <WiFi.h>

#include "esp_now.h"

void mac_address();

class EspNow{
    public:
        EspNow(
            uint8_t mac_address[6]
        );

        void setup(bool state);
        bool getState();
        esp_err_t send_mensage(const uint8_t* pic_buf, size_t length);


    private:
        uint8_t broadcast_address[6];
        esp_now_peer_info_t peerInfo;
};

#endif