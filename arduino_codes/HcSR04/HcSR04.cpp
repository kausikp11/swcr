/*
  Hc-SR04.cpp - Library for SWCR code.
  Created by Kausik P, February 16, 2020.
*/
#include "Arduino.h"
#include "HcSR04.h"

HcSR04::HcSR04(int Trig, int Echo)
{
  pinMode(Trig, OUTPUT);
  pinMode(Echo, INPUT);
  _Trig = Trig;
  _Echo = Echo;
}
double HcSR04::sense()
{
  digitalWrite(_Trig, LOW);
  delayMicroseconds(2);
  digitalWrite(_Trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(_Trig, LOW);
  duration = pulseIn(_Echo, HIGH);
  distance = duration * 0.034 / 2;
  return distance;
}
