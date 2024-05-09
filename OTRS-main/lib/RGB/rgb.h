#ifndef RGB
#define RGB

//todos desligados
#define OFF 0

//cores primarias 
#define RED 1
#define GREEN 2
#define BLUE 4

//cores secundarias
#define YELLOW (RED + GREEN)
#define CYAN (GREEN + BLUE)
#define PURPLE (RED + BLUE)

//todos acesos
#define WHITE (RED + GREEN + BLUE)

#include "Arduino.h"

class LedRGB{
  private:
    int led_r_pin;
    int led_g_pin;
    int led_b_pin;

  public:
    LedRGB(int led_r, int led_g, int led_b);
    int getRPin();
    int getGPin();
    int getBPin();
    void rgbInit();
    void rgbColor(int led);
    void turnOn(int led);
    void turnOff(int led);
};

#endif
