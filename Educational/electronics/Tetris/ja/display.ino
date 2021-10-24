unsigned long long mainImage[4] = {2,20,200,2000};
byte oneBits[8] = {1,2,4,8,16,32,64,128};
short count = 1;
short secCount = 0;
long timer = 0;
volatile short vLine = 0;

void syncV(){
  vLine = 0;
}

void setLine(){
  byte line[2];
  short lineI = vLine;
  bool secDisp = false;
  if (vLine >= 8)
    secDisp = true;
  for(int i = 0; i < 2; i++){
    unsigned long long imgPart = mainImage[i];
    if(secDisp)
      imgPart = mainImage[i+2];
    unsigned long long lineAnder = 18374686479671623680; //første 8 bits høje
    int maxj = vLine;
    if (secDisp)
      maxj -= 8;
    printLine = maxj;
    for (int j = 0; j < maxj; j++){
      lineAnder = lineAnder >> 8;
    }
    printByteLine((lineAnder & imgPart) >> (64-(8-maxj)*8));
  }
  vLine++;
}

void printByteLine(byte line){
  for (int i = 0; i < 8; i++){
    if(oneBits[i] & line){
      digitalWrite(serialPin, HIGH);
      digitalWrite(clockPin, HIGH);
      delayMicroseconds(1);
      digitalWrite(clockPin, LOW);
      digitalWrite(serialPin, LOW);
    }
    else
      digitalWrite(clockPin, HIGH);
      delayMicroseconds(1);
      digitalWrite(clockPin, LOW);
  }
}
