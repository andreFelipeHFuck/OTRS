#include "EspNow.h"

bool espNowState = false;

void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t sendStatus){
    if(sendStatus == ESP_NOW_SEND_SUCCESS)
        Serial.println("Mensage sucess send");
    else
        Serial.println("Fall send mensage");

    espNowState = true;
}

void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len){
    for(int i=0; i<len; i++)
        Serial.println(incomingData[i]);    
}

void mac_address(){
    delay(500);

    Serial.println();
    Serial.print("MAC address: ");
    Serial.println(WiFi.macAddress());
}

EspNow::EspNow(uint8_t mac_address[6]){
    memcpy(peerInfo.peer_addr, broadcast_address, 6);
}

void EspNow::setup(bool state){
  memcpy(peerInfo.peer_addr, broadcast_address, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  if(state)
    WiFi.mode(WIFI_STA);

  if (esp_now_init() != ESP_OK){
    Serial.println("Error iniciate ESP-NOW");
    return;
  }

  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Erro ao adicionar o receptor ao whitelist");
    return;
  }

  esp_now_register_send_cb(OnDataSent);
  //esp_now_register_recv_cb(OnDataRecv);
}

bool EspNow::getState(){
    return espNowState;
}

esp_err_t EspNow::send_mensage(const uint8_t* pic_buf, size_t length){
   
    if (esp_now_send(broadcast_address, pic_buf, length) != ESP_OK) {
        Serial.println("Erro ao enviar a mensagem");
    }

    espNowState = false;
}
