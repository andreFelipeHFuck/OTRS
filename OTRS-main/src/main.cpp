#include <Arduino.h>
#include <Camera.h>
#include <Mqtt.h>

#include "base64.h"

Camera camera(1);

Mqtt mqtt(
   "ANDRE 7824",
   "463Mp9,5",
   "10.90.34.49",
   1883,
   "",
   "",
   "imagem/sub",
   "imagem/pub"
);

void publish(const uint8_t* pic_buf, size_t length){
  mqtt.pub_topic(pic_buf, length);
}

void take_photo(){
  Serial.println(mqtt.getState());

  if(mqtt.getState()){
      Serial.print("Estado: ");
      camera.take_photo(publish);
  }
}

void setup() {
  Serial.begin(115200);
  
  mqtt.setup();
  camera.setup();
}

void loop() {
  mqtt.teste_topic();

  take_photo();  
}