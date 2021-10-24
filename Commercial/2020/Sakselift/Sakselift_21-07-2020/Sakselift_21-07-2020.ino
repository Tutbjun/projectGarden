//
//You might have to power cycle the uStepper board upon loading code, wierd glitch.
//
#include <uStepperS.h>



uStepperS stepper;
const int homeSwitchPin = 8;
const int topSwitchPin = 7;
const int buttonPin1 = 6;
const int buttonPin2 = 2;

const int preHomingPos = -100; //the angle at wich the stepper parks before doing the homing operation after a move
const bool runClosedLoop = false;

//default profile
const int currentValDefault = 90; //equates to the force
const int speedDefault = 400; //the speed that it runs with if nothing else is specified

//position 1 profile
const int positionOne = -2000; //position 1 in degrees of stepper rotation  //negative value for CCW, positive for CW
const int currentValOne = 90;
const int speedOne = 400;
const int waitTimeOne = 1000;

//position 2 profile
const int positionTwo = -9000; //position 2 in degrees of stepper rotation
const int currentValTwo = 90;
const int speedTwo = 400;
const int waitTimeTwo = 1000;

//position 2 profile
const int positionThree = -12000; //position 3 in degrees of stepper rotation
const int currentValThree = 90;
const int speedThree = 400;
const int waitTimeThree = 1000;

int x = 0;
bool unitHomed = false; //ceeps track of wether the unit is homed

void setup() {
  resetStepper();//resets encoder
  
  stepper.checkOrientation(10.0);       //Check orientation of motor connector
  stepper.setCurrent(currentValDefault);
  stepper.setHoldCurrent(0); 
  stepper.setMaxVelocity(speedDefault); //MAX speed when going between waypoints

  //MAX - degrees 12500 degrees around 60cm of lift

  Serial.begin(9600);
  //stepper.setRPM(100);
  pinMode(homeSwitchPin , INPUT);
  pinMode(topSwitchPin , INPUT);
  pinMode(buttonPin1 , INPUT);
  pinMode(buttonPin2, INPUT);
  homing();

}

void loop() {
  char cmd;
  
  cmd = Serial.read();
  //while(!Serial.available());
  //Serial.println(stepper.encoder.getAngleMoved()); //spits out the absolute position
  if(digitalRead(buttonPin1) == LOW || digitalRead(buttonPin2) == LOW)
    delay(100);//waits to ensure that the pin voltages has stabilised
  
  if(digitalRead(buttonPin1)== LOW && digitalRead(buttonPin2)== HIGH && digitalRead(topSwitchPin)== HIGH)                     
   {
    Serial.println("button1");
    moveTo(positionOne,currentValOne,speedOne,waitTimeOne);
   }
    
  else if(digitalRead(buttonPin2)== LOW && digitalRead(buttonPin1)== HIGH && digitalRead(topSwitchPin)== HIGH)
  {
    Serial.println("button1");
    moveTo(positionTwo,currentValTwo,speedTwo,waitTimeTwo);     
   }
  else if(digitalRead(buttonPin2)== LOW && digitalRead(buttonPin1)== LOW && digitalRead(topSwitchPin)== HIGH)//if both are low, then a third signal is sent
  {
    Serial.println("button3");
    moveTo(positionThree,currentValThree,speedThree,waitTimeThree);     
   }
  else if(digitalRead(topSwitchPin)== HIGH && unitHomed == false)  
  {
    homing();  
    }
  else if(cmd == '3')                 
    {
     homing();
    } 
  delay(50);

}

void moveTo(int Position,int CurrentVal,int Speed,int WaitTime)
{
  stepper.setCurrent(CurrentVal);//sets specified peremiters
  stepper.setMaxVelocity(Speed);
  
  do{//moves to position
    stepper.moveToAngle(Position);
    x = stepper.encoder.getAngleMoved();
    } while (x > Position);
  delay (WaitTime);
  
  do{//moves back to parking position
    Serial.print(" " + x);
    stepper.moveToAngle(preHomingPos);
    x = stepper.encoder.getAngleMoved();
    } while (x < preHomingPos); 
     
  homing();
  
  stepper.setCurrent(currentValDefault);//resets peremiters
  stepper.setMaxVelocity(speedDefault);
}

void homing() { //goes back until it is jamed, then resets position to 0
  
  //homing config
  int homingTrustFactor = 5; //the amount of reading it takes before it decides that it is jamed
  int minHomingTime = 200; //this is to counteract acceleration time
  stepper.setCurrent(40); //the force with wich it homes with
  int homingSpeed = 100;
  //

  int lastxs[homingTrustFactor]; //the aray holding the measurred position
  bool homingFinished;
  int homingTimeElapsed = 0; //used for creating a min. homing time
  int homingStartTime = millis();
  
  do{
    homingTimeElapsed = millis() - homingStartTime; //sets ellapsed time
    
    for(int i = homingTrustFactor-1; i > -1; i--) //stores positional values
      lastxs[i] = lastxs[i-1];
    lastxs[0] = x;
    Serial.println(x);
    stepper.setRPM(homingSpeed); //starts movement
    
    x = stepper.encoder.getAngleMoved(); //reads position

    homingFinished = true; //will most likely be set false by the folowing code
    for(int i = 0; i < homingTrustFactor-1; i++) //checks wether the motor is jamed
      if(lastxs[i] != lastxs[i+1])
        homingFinished = false;
    if (minHomingTime > homingTimeElapsed) //checks wether enough time has ellapsed
      homingFinished = false;
    } while (homingFinished == false); //continues homing if not finished
  
  stepper.stop(SOFT); //stops softly
  delay(200);
  resetStepper(); //resets encoders position to 0
  stepper.setCurrent(currentValDefault);

  unitHomed = true;
}

void resetStepper(){
  if(runClosedLoop)
    stepper.setup(CLOSEDLOOP,200); 
  else if(!runClosedLoop)
    stepper.setup(NORMAL,200); 
}
