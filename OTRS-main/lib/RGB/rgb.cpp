#include "rgb.h"

LedRGB::LedRGB(int led_r, int led_g, int led_b):
led_r_pin(led_r),
led_g_pin(led_g),
led_b_pin(led_b)
{}

 int LedRGB::getRPin(){return led_r_pin;}
 int LedRGB::getGPin(){return led_g_pin;}
 int LedRGB::getBPin(){return led_b_pin;}

void LedRGB::rgbInit(){
  pinMode(led_r_pin, OUTPUT);
  pinMode(led_g_pin, OUTPUT);
  pinMode(led_b_pin, OUTPUT);
}

void LedRGB::rgbColor(int led){
  if(led & 1){
    digitalWrite(led_r_pin, HIGH);
  }else{
    digitalWrite(led_r_pin, LOW);
  }

  if(led & 2){
    digitalWrite(led_g_pin, HIGH);
  }else{
    digitalWrite(led_g_pin, LOW);
  }

  if(led & 4){
    digitalWrite(led_b_pin, HIGH);
  }else{
    digitalWrite(led_b_pin, LOW);
  }
}

void LedRGB::turnOn(int led){
  if(led & 1){
    digitalWrite(led_r_pin, HIGH);
  }

  if(led & 2){
    digitalWrite(led_g_pin, HIGH);
  }

  if(led & 4){
    digitalWrite(led_b_pin, HIGH);
  }
}

void LedRGB::turnOff(int led){
  if(led & 1){
    digitalWrite(led_r_pin, LOW);
  }

  if(led & 2){
    digitalWrite(led_g_pin, LOW);
  }

  if(led & 4){
    digitalWrite(led_b_pin, LOW);
  }
}
