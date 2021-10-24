#include <SoftwareSerial.h>//inkluderer seriel emitering til bluetooth modulet

//autokøring værdier
float Kp = 0.55;
float Ki = 1.16;
float Kd = 0.33;
float speedVal = 1.44;
int motorLowest = 80;


int sensorAntal = 5; //giver sig selv
uint8_t sensorPins[5] = {A0, A1, A2, A3, A4};//laver en serie til sensorinput og rækkefølge
float sensorBer[5] = {-170,-483,-276,-215,-98};//forskydningsværdier og standartkalibreringværdier
float sensorAer[5] = {1.55, 1.99, 1.41, 1.31, 1.63};//hældningsværdier og standartkalibreringværdier
int sensorInterval = 1000;//normaliseringsværdi til kalibrering

int ledPin = 4;//pins til interface til kalibrering
int knapPin = 7;

long sidsteTid = 0;//bruges til intervallet for sensorudskrivning
long udskrivTid = 1000;//udskrivningsinterval

const int motor1A = 5;//pins for motorerne
const int motor1B = 6;
const int motor2A = 9;
const int motor2B = 10;

long acc = 0;//drejekoeficient fra PID

const int shootPin = 12;//pin til skyder

int bluetoothTx=2;//bluetooth seriel pins
int bluetoothRx=3;
SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);//starter serielemitering på angivne pins som bluetooth objektet
char data;//modtaget data

bool pidON = false;//autokørsel tænd/sluk

void setup() {
  //sætter pinmodes
  pinMode(ledPin, OUTPUT);
  pinMode(knapPin, INPUT);

  pinMode(motor1A, OUTPUT);
  pinMode(motor1B, OUTPUT);
  pinMode(motor2A, OUTPUT);
  pinMode(motor2B, OUTPUT);

  pinMode(shootPin, OUTPUT);

  //sætter baudrate på de to seriel forbindelser
  Serial.begin(9600);
  bluetooth.begin(115200);
}

void loop() {
  bluetooth_();//finder og eksekverer ordrer fra bluetooth
  
  float sensorDat[sensorAntal];//serie af modtaget sensordata
  for (int i = 0; i < sensorAntal; i++) {
    sensorDat[i] = analogRead(sensorPins[i]);//læser sensorer
  }
  /*if (millis() > sidsteTid + udskrivTid) {
    Serial.println("sensorDatRå:");
    for (int i = 0; i < sensorAntal; i++) {
      Serial.println(sensorDat[i]);
    }
  }*/
  for (int i = 0; i < sensorAntal; i++) {//sætter kalibreringsværdier på modtaget data
    sensorDat[i] += sensorBer[i];
    sensorDat[i] *= sensorAer[i];
  }
  
  for(int i = 0; i < sensorAntal; i++){//sætter cutoff værdier på modtaget data
    if(sensorDat[i] > sensorInterval){
      sensorDat[i] = sensorInterval;
    }
    if(sensorDat[i] < 0){
      sensorDat[i] = 0;
    }
  }
  
  if (digitalRead(knapPin)==HIGH) {//hvis der trykkes på knappen, så kører den kalibreringsfunktionen
    kalibrerSensor();
  }

  //for hvert sekund udskrives alle data
  if (millis() > sidsteTid + udskrivTid) {
    Serial.println("sensorDatKal:");
    for (int i = 0; i < sensorAntal; i++) {
      Serial.println(sensorDat[i]);
    }
    sidsteTid = (long)millis(); 
  }

  //hvis der er autostyring, så skal der udregnes en drejehastighed og motorne skal sættes til at køre med det  
  if(pidON){
    acc = accPID(sensorDat);
    drive(motorLowest);
  }
  Serial.println(acc);
}
