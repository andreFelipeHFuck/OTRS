#include <Arduino.h>
#include <Camera.h>
#include <MqttPub.h>

#include "base64.h"

Camera camera(1);

MqttPub mqttPub(
   "ANDRE 7824",
   "463Mp9,5",
   "192.168.100.89",
   1883,
   "",
   "",
   "imagem"
);

void publish(const uint8_t* pic_buf, size_t length){
  mqttPub.pub_topic(pic_buf, length);
}

void setup() {
  Serial.begin(115200);
  
  mqttPub.setup();
  camera.setup();

  mqttPub.teste_topic();
   
  camera.take_photo(publish);
}

void loop() {

  
}