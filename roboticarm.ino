#include <Servo.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo gripper;

int servoPositions[4];
int currentAngle[4]  = {0, 0, 180, 0};  // dat 1 chuoi gia tri ban dau de so sanh

void setup() {
  Serial.begin(9600);
  base.attach(3);
  shoulder.attach(5);
  elbow.attach(6);
  gripper.attach(9);

  // Thiet lap trang thai ban dau cho robot
  base.write(0);
  shoulder.write(0);
  elbow.write(180);
  gripper.write(0);
}
void Servo_actions(int index, int new_angle)    // so sanh goc moi nhan tu serial voi goc hien tai
{
  if(currentAngle[index] < new_angle)
  {
    for(int i = currentAngle[index]; i < new_angle; i+=2)
    {
      if(index == 0)
      {
        base.write(i);
      }
      else if(index == 1)
      {
        shoulder.write(i);
      }
      else if(index == 2)
      {
        elbow.write(i);
      }
      else if(index == 3)
      {
        gripper.write(i);
      }
      delay(15);
    }
    currentAngle[index] = new_angle;
  }
  else if(currentAngle[index] > new_angle)    
  {
    for(int i = currentAngle[index]; i > new_angle; i-=2)
    {
        if(index == 0)
        {
          base.write(i);
        }
        else if(index == 1)
        {
          shoulder.write(i);
        }
        else if(index == 2)
        {
          elbow.write(i);
        }
        else if(index == 3)
        {
          gripper.write(i);
        }
        delay(15);
    }
    currentAngle[index] = new_angle;
  }
}
void loop() {

  while(Serial.available()){
    String input = Serial.readStringUntil('\n');
    servoPositions[0] = input.substring(0,3).toInt();
    servoPositions[1] = input.substring(3,6).toInt();
    servoPositions[2] = input.substring(6,9).toInt();
    servoPositions[3] = input.substring(9,12).toInt();
    Servo_actions(0, servoPositions[0]);
    Servo_actions(1, servoPositions[1]);
    Servo_actions(2, servoPositions[2]);
    Servo_actions(3, servoPositions[3]);
    delay(100);
  }
}
