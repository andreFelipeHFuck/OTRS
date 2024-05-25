#include "Camera.h"

// mfb.listas@gmail.com

//Private
Camera::Camera(bool flash):
flash(flash)
{}  

void Camera::setup(){
    pinMode(FLASH_PIN, OUTPUT);
    config = config_camera();
    verify_config_camera(config);
}

void Camera::verify_config_camera(camera_config_t config){
    esp_err_t err = esp_camera_init(&config);

    if(err != ESP_OK){
        Serial.printf("Iniciar camera falhou erro )x%x", err);
        delay(1000);
        ESP.restart();
    }
}

camera_config_t Camera::config_camera(){
     camera_config_t config;

    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sscb_sda = SIOD_GPIO_NUM;
    config.pin_sscb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;
    config.frame_size =  FRAMESIZE_XGA;  
    config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
    config.fb_location = CAMERA_FB_IN_PSRAM;
    config.jpeg_quality = 12;
    config.fb_count = 1;

     if (config.pixel_format == PIXFORMAT_JPEG) {
        if (psramFound()) {
        config.jpeg_quality = 14;
        config.fb_count = 1;
        config.grab_mode = CAMERA_GRAB_LATEST;
        config.frame_size = FRAMESIZE_XGA;
        } else {
        config.frame_size = FRAMESIZE_SVGA;
        config.fb_location = CAMERA_FB_IN_DRAM;
        }
     } else {
        config.frame_size = FRAMESIZE_SVGA;
    #if CONFIG_IDF_TARGET_ESP32S3
        config.fb_count = 2;
    #endif
    }


    return config;
}

void Camera::take_photo_flash(Funcao f){    
    digitalWrite(FLASH_PIN, flash ? HIGH : LOW);
    delay(100);

     fb = esp_camera_fb_get();

    digitalWrite(FLASH_PIN, LOW);
    delay(100);

    if(!fb){
        Serial.println("Camera capture failed");
        ESP.restart();
        return;
    }

    Serial.println("Camera capture sucess");

    /*
    if(fb->format != PIXFORMAT_JPEG){
        Serial.println("Non-JPEG data not implemented");
        esp_camera_fb_return(fb);
        return;
    }*/

    f(fb->buf, fb->len);

    Serial.println("Photo send to mqtt sucess");

    esp_camera_fb_return(fb);
}

//Public
void Camera::take_photo(Funcao f){
    take_photo_flash(f);
}
