#ifndef CAMERA
#define CAMERA

#include <Arduino.h>
#include "esp_camera.h"

#include <MqttPub.h>

// Pinos

#define PWDN_GPIO_NUM  32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM  0
#define SIOD_GPIO_NUM  26
#define SIOC_GPIO_NUM  27

#define Y9_GPIO_NUM    35
#define Y8_GPIO_NUM    34
#define Y7_GPIO_NUM    39
#define Y6_GPIO_NUM    36
#define Y5_GPIO_NUM    21
#define Y4_GPIO_NUM    19
#define Y3_GPIO_NUM    18
#define Y2_GPIO_NUM    5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM  23
#define PCLK_GPIO_NUM  22

#define FLASH_PIN 4

typedef void (*Funcao) (const uint8_t*, size_t);

class Camera
{
    public:
       Camera(bool flash);

       camera_fb_t* getFb();
       void setup();
       void take_photo(Funcao f);

    private:
        bool flash;
        camera_config_t config;

        camera_fb_t *fb = NULL;

        void verify_config_camera(camera_config_t config);
        camera_config_t config_camera();

        void take_photo_flash(Funcao f);
        void transform_image();
};


#endif