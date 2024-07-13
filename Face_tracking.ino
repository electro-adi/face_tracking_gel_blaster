#include <ESP32Servo.h>

#define servoX_pin 15
#define servoY_pin 2
#define servoTrig_pin 4

Servo servoX;
Servo servoY;
Servo servoTrig;

int count;

String inputString;

void setup()
{
  ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);

	servoX.setPeriodHertz(50);
	servoX.attach(servoX_pin, 500, 2500);

	servoY.setPeriodHertz(50);
	servoY.attach(servoY_pin, 500, 2500);

  servoTrig.setPeriodHertz(50);
	servoTrig.attach(servoTrig_pin, 500, 2500);

  servoX.write(90);
  servoY.write(90);//max 115 min 70
  servoTrig.write(0);

  Serial.begin(9600);
}


void loop()
{
  while(Serial.available())
  {
    inputString = Serial.readStringUntil('\r');

    // Find the first comma and extract the first value
    int firstCommaIndex = inputString.indexOf(',');
    int x_axis = inputString.substring(0, firstCommaIndex).toInt();

    // Find the second comma and extract the second value
    int secondCommaIndex = inputString.indexOf(',', firstCommaIndex + 1);
    int y_axis = inputString.substring(firstCommaIndex + 1, secondCommaIndex).toInt();

    // Extract the third value (after the second comma)
    int detected = inputString.substring(secondCommaIndex + 1).toInt();

    servoX.write(x_axis);

    //inverting y axsis servo values
    int inverted_y_axis = 180 - y_axis;
    servoY.write(inverted_y_axis);

    if(detected == 1)
    {
      count++;
    }
    else
    {
      count = 0;
      servoTrig.write(0);//trigger off
    }

    if(count > 15)
    {
      servoTrig.write(90);//trigger on
    }
  }
}
