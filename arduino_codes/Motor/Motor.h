/*
  Motor.h - Library for SWCR Motor code.
  Created by Kausik P, February 9, 2020.
*/
#ifndef Motor_h
#define Motor_h
#include"Arduino.h"
class Motor
{
  public:
    Motor(int IN1, int IN2, int IN3, int IN4, int ENA, int ENB);
    void Motor_move(int Pulse_Width1,int Pulse_Width2);
  private:
    int _IN1;
    int _IN2;
    int _IN3;
    int _IN4;
    int _ENA; 
    int _ENB;
  };

#endif
