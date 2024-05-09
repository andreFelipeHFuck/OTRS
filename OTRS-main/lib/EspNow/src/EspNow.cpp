#include "EspNow.h"

void OnDataSent(uint8_t *mac_addr, uint8_t sendStatus);

void OnDataRecv(uint8_t * mac, uint8_t *incomingData, uint8_t len);

void mac_address(){
    delay(500);

    Serial.println();
    Serial.print("MAC address: ");
    Serial.println(WiFi.macAddress());
}

EspNowSend::EspNowSend(uint8_t mac_address[6]){
    for(int i=0; i < 6; i++){
        broadcast_address[i] = mac_address[i];
    }
}

void EspNowSend::setup(){
    WiFi.mode(WIFI_STA);

    if (esp_now_init() != 0){
        Serial.println("Error iniciate ESP-NOW");
        delay(1000);
        ESP.restart();
    }

    //esp_now_register_send_cb(OnDataSent);

   // esp_now_add_peer(broadcast_address, ESP_NOW_ROLE_SLAVE, 1)
}

esp_err_t EspNowSend::send_mensage(){
    return 0;
}
