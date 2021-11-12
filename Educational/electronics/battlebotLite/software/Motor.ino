//sætter hastigheder for bluetoothstyring
int turnSpeed = 100;                            //sætter rotationshastighede
int moveSpeed = 255;                            //sætter bevægelseshastighede

//funktionen der får robotten til at køre fremad
void foward() {                           
  digitalWrite(motor1A,LOW);                    //sætter venstre motor til at køre fremad                  
  analogWrite(motor1B,moveSpeed);               //sætter hastighed til venstre motor 
  digitalWrite(motor2A,LOW);                    //sætter højre motor til at køre fremad 
  analogWrite(motor2B,moveSpeed);               //sætter hastighed til højre motor 
}

//funktionen der får robotten til at køre baglens
void backward() {                               
  analogWrite(motor1A,moveSpeed);               //sætter hastighed til venstre motor
  digitalWrite(motor1B,LOW);                    //sætter venstre motor til at køre baglens 
  analogWrite(motor2A,moveSpeed);               //sætter hastighed til højre motor
  digitalWrite(motor2B,LOW);                    //sætter højre motor til at køre baglens 
}

//funktionen der får robotten til at køre til højre
void turnRight() {
  analogWrite(motor1A,turnSpeed);               //sætter hastighed til venstre motor
  digitalWrite(motor1B,LOW);                    //sætter venstre motor til at køre baglens
  digitalWrite(motor2A,LOW);                    //sætter højre motor til at køre forlens
  analogWrite(motor2B,turnSpeed);               //sætter hastighed til højre motor
}

//funktionen der bliver kaldt når robotten skal køre venstre
void turnLeft() {
  digitalWrite(motor1A,LOW);                    //sætter venstre motor til at køre fremad
  analogWrite(motor1B,turnSpeed);               //sætter hastighed til venstre motor
  analogWrite(motor2A,turnSpeed);               //sætter hastighed til højre motor
  digitalWrite(motor2B,LOW);                    //sætter højre motor til at køre bagud
}

//funktionen der får robotten til at stoppe med at køre
void stop_() {
  //stopper begge motorer
  digitalWrite(motor1A,LOW);                
  digitalWrite(motor1B,LOW); 
  digitalWrite(motor2A,LOW);
  digitalWrite(motor2B,LOW);
}

//funktionen der får robotten til at at snurre rundt til højre
void spinbot() {
  //robotten snurre til højre med fuld fart
  //venstre motor sættes til at køre fremad med fuld fart
  digitalWrite(motor1A,HIGH);               
  digitalWrite(motor1B,LOW);
  //højre motor sættes til at køre baglens med fuld fart
  digitalWrite(motor2A,LOW);
  digitalWrite(motor2B,HIGH); 
}

//funktion for skyderen til at skyde
void kaShoot() { 
  //sætter skydepin til høj i 0,9 s. for at skyde et sekundt                            
  digitalWrite(shootPin,HIGH);
  delay(90);                                    //delay som styrer at den kun affyre et skud
  digitalWrite(shootPin,LOW); 
}

//autokørsel funktion der modtager min. hastighed
void drive(int lowest) {
  if(sensorAer[0] != 0){//tjekker at sensorerne er kalibreret
    float Lspeed = (float)(lowest + acc)*speedVal;//udregner de to motorers hastigheder
    float Hspeed = (float)(lowest - acc)*speedVal;
    if(Lspeed < 0)                                
      Lspeed = 0;                                 //sætter hastigheden på venstre motor til 0, hvis den er negativ
    if(Lspeed > 255)
      Lspeed = 255;                               //sætter hastigheden på venstre motor til 255, hvis den er for høj
    if(Hspeed < 0)
      Hspeed = 0;                                 //sætter hastigheden på højre motor til 0, hvis den er negativ
    if(Hspeed > 255)
      Hspeed = 255;                               //sætter hastigheden på højre motor til 255, hvis den er for høj
    digitalWrite(motor1A,LOW);                    //sætter venstre motor til at køre fremad
    analogWrite(motor1B,Lspeed);                  //sætter hastigheden til venstre motor
    digitalWrite(motor2A,LOW);                    //sætter højre motor til at køre fremad
    analogWrite(motor2B,Hspeed);                  //sætter hastigheden til høre motor
  }
}
