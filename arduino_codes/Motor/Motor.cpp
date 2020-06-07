/*
  Motor.cpp - Library for SWCR Motor code.
  Created by Kausik P, February 9, 2020.
*/

#include "Arduino.h"
#include "Motor.h"

Motor::Motor(int IN1, int IN2, int IN3, int IN4, int ENA, int ENB)
{
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  _IN1 = IN1;
  _IN2 = IN2;
  _IN3 = IN3;
  _IN4 = IN4;
  _ENA = ENA;
  _ENB = ENB;
}
void Motor::Motor_move(int Pulse_Width1,int Pulse_Width2){
 if (Pulse_Width1 > 0){
     analogWrite(_ENA, Pulse_Width1);
     digitalWrite(_IN1, HIGH);
     digitalWrite(_IN2, LOW);
 }
 if (Pulse_Width1 < 0){
     Pulse_Width1=abs(Pulse_Width1);
     analogWrite(_ENA, Pulse_Width1);
     digitalWrite(_IN1, LOW);
     digitalWrite(_IN2, HIGH);
 }
 if (Pulse_Width1 == 0){
     analogWrite(_ENA, Pulse_Width1);
     digitalWrite(_IN1, LOW);
     digitalWrite(_IN2, LOW);
 }
 if (Pulse_Width2 > 0){
     analogWrite(_ENB, Pulse_Width2);
     digitalWrite(_IN3, LOW);
     digitalWrite(_IN4, HIGH);
 }
 if (Pulse_Width2 < 0){ 
     Pulse_Width2=abs(Pulse_Width2);
     analogWrite(_ENB, Pulse_Width2);
     digitalWrite(_IN3, HIGH);
     digitalWrite(_IN4, LOW);
 }
 if (Pulse_Width2 == 0){
     analogWrite(_ENB, Pulse_Width2);
     digitalWrite(_IN3, LOW);
     digitalWrite(_IN4, LOW);
 }
}
