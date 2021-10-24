int interruptPin = 2;
int serialPin = 6;
int clockPin = 7;
int vsyncPin = 3;
int fpsPin = 5;

unsigned long long blockImage[4];
unsigned long long envImage[4];
unsigned short int rotation = 0;

unsigned long long printLine;//temp

void setup() {
  pinMode(interruptPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(interruptPin), setLine, RISING);
  pinMode(vsyncPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(vsyncPin), syncV, FALLING);
  pinMode(serialPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(fpsPin,OUTPUT);
  analogWrite(fpsPin,127);
  Serial.begin(9600);

  int prescalerVal = 0x07;
  TCCR0B &= ~prescalerVal;
  prescalerVal = 4;
  TCCR0B |= prescalerVal;
}

bool up = false;
bool down = false;
bool right = false;
bool left = false;
bool space = false;
bool hold = false;

void loop() {
  Serial.println(uint32_t(printLine));
//  Serial.print(long(printLine));
  tjekInputs();
  if(up){
    
  }
  //Vent til timeren siger ny frame
    //tjekFlyt()
    //tjekRot(rot, flyt)
    
    
    //læs inputs
    //roter
      //tjek om den kan rotere et sted hen med metoden
        //hvis ikke, så lad værre
        //hvis så gøre det
    //flyt sidelæns
      //tjek om den kan
        //hvis ja, så flyt
        //hvis nej, så las værre
    //flyt helt ned
      //hvad er det laveste den kan flyttes til?
      //flyt dertil
      //tilføj blok til samlet array
      //skift til næste blok i køen
      //opdater kø
    //hold
      //tjek om den i hold kan placeres et sted
        //hvis ja skift
        //hvis nej, bare fortsæt
        
    //flytned
      //tjek om den kan flytte ned
        //hvis ikke, så count op på en int der afgører hvornår blokken skal stå fast
        //hvis den kan, så bare flyt ned
          //og nulstil den der int
  
    //hvis den der counter int er nået en bestemt threshold
      //gør blokken til en del af det samlede array
      //skift til næste blok i køen
      //opdater kø
}
