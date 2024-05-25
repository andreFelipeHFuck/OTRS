#include <Arduino.h>

#include <Camera.h>
#include <Mqtt.h>


Camera camera(true);

Mqtt mqtt(
   "ANDRE 7824",
   "463Mp9,5",
   "192.168.100.89",
   1883,
   "",
   "",
   "imagem/request_image",
   "imagem/send_image"
);

void publish(const uint8_t* pic_buf, size_t length){
  mqtt.pub_topic(pic_buf, length);
}

void take_photo(){
  //Serial.println(mqtt.getState());

  if(mqtt.getState()){ 
      camera.take_photo(publish);
  }
}

void setup() {
  Serial.begin(115200);
  
  camera.setup();
  
  mqtt.setup();

}

void loop() {
  
  mqtt.teste_topic();

  take_photo();  

}