#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdbool.h>
#include <util/delay.h>
#define MAX_STR 50
#define BAUD 9600


int pinAnalogico1 = 14; //sensor PH
int pinAnalogico2 = 15; //Sensor CO2
int pinAnalogico3 = 16; //Sensor Temperatura
int pinAnalogico4 = 17; //Sensor Luz

int bomba=3;
int foco=4;
int ventilador=5;


void setup() 
{
//Configuro interrupcion por TIMER
TCCR1A = 0;  // El registro de control A queda todo en 0, pines OC1A y OC1B deshabilitados
TCCR1B = 0;  // Limpia el registrador
TCCR1B |= (1<<CS10)|(1 << CS12);   // configura prescalador para 1024
TCNT1 =0xC2F8;  // inicia timer para desbordamiento 1 Segundo
TIMSK1 |= (1 << TOIE1); //Habilito la interrupcion por desboradmiento.
 
pinMode (pinAnalogico1,INPUT); //Establesco pin 14 como entrada 
pinMode (pinAnalogico2,INPUT); //Establesco pin 15 como entrada
pinMode (pinAnalogico3,INPUT); //Establesco pin 16 como entrada
pinMode (pinAnalogico4,INPUT); //Establesco pin 17 como entrada

pinMode (bomba,OUTPUT); //Establesco pin 3 como salida
pinMode (foco,OUTPUT); //Establesco pin 4 como salida
pinMode (ventilador,OUTPUT); //Establesco pin 5 como salida

Serial.begin(9600); // Habilito comunicacion serial a 9600 baudios

}

ISR(TIMER1_OVF_vect)   //Establesco lo que sucede en la interrupcion
{
   TCNT1 = 0xC2F7; // Se renicia el TIMER
   char accion = Serial.read(); //Recibo dato del atmega por RX
   accion -= '0';

   if ((int)accion==2) //Si la accion es ON bomba
   {
     digitalWrite(bomba,  HIGH);
   }
   if ((int)accion==3) //Si la accion es ON foco
   {
     digitalWrite(foco,  HIGH);
   }
   if ((int)accion==4) //Si la accion es ON ventilador
   {
     digitalWrite(ventilador,  HIGH);
   }
   if ((int)accion==5) //Si la accion es OFF bomba
   {
     digitalWrite(bomba,  LOW);
   }
   if ((int)accion==6) //Si la accion es OFF foco
   {
     digitalWrite(foco,  LOW);
   }
   if ((int)accion==7) //Si la accion es OFF ventilador
   {
     digitalWrite(ventilador,  LOW);
   }
   
}

void loop() {

int valorPinAnalogico1 = analogRead(pinAnalogico1); //Lectura del valor de entrada en el pin 14
Serial.println("2000");  //Envio identificador
delay(100);
Serial.println(valorPinAnalogico1); //Envio valor sensor PH por puerto serial TX
delay(400);
int valorPinAnalogico2 = analogRead(pinAnalogico2); //Lectura del valor de entrada en el pin 15
Serial.println("3000");  //Envio identificador
delay(100);
Serial.println(valorPinAnalogico2); //Envio valor sensor CO2 por puerto serial TX
delay(400);
int valorPinAnalogico3 = analogRead(pinAnalogico3); //Lectura del valor de entrada en el pin 16
float millivolts = (valorPinAnalogico3 / 1024.0) * 5000;
int celsius = (millivolts) / 10; 
Serial.println("4000");  //Envio identificador
delay(100);
Serial.println(celsius);//Envio valor sensor Temperatura por puerto serial TX
delay(400);
int valorPinAnalogico4 = analogRead(pinAnalogico4); //Lectura del valor de entrada en el pin 17
Serial.println("5000");  //Envio identificador
delay(100);
Serial.println(valorPinAnalogico4); //Envio valor sensor Luz por puerto serial TX
delay(1500);


}

