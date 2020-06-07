/*
  Hc-SR04.h - Library for SWCR code.
  Created by Kausik P, February 16, 2020.
*/
#ifndef HcSR04_h
#define HcSR04_h
#include "Arduino.h"
class HcSR04
{
  public:
    HcSR04(int Trig,int Echo);
    double sense();
  private:
    int _Trig;
    int _Echo;
    int duration;
    double distance;
};
#endif
