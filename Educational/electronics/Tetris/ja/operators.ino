unsigned long long bitToNumber(long byte4,long byte3,long byte2,long byte1){//meget ineffektiv, kun til debug
  long number = 0;
  if(byte4 != 0){
    number += byteToNumber(byte1,0);
    number += byteToNumber(byte2,8);
    number += byteToNumber(byte3,16);
    number += byteToNumber(byte4,24);
  }
  else if(byte3 != 0){
    number += byteToNumber(byte1,0);
    number += byteToNumber(byte2,8);
    number += byteToNumber(byte3,16);
  }
  else if(byte2 != 0){
    number += byteToNumber(byte1,0);
    number += byteToNumber(byte2,8);
  }
  else if(byte1 != 0){
    number += byteToNumber(byte1,0);
  }
  return number;
}

long byteToNumber(long input,byte bitsOffset){
  long number = 0;
  for (int i = 0; i < 8; i++){
    float decPos = long(pow(10,i+1)+0.5);
    long remainder = long(long(input / decPos+0.5)*decPos+0.5);
    if(input - remainder > decPos*0.05){
      number += long(pow(2,i+bitsOffset)+0.5 );
    }
  }
  return number;
}

bool tjekOverlap(unsigned long long part1[4], unsigned long long part2[4]){
  for(int i = 0; i < 4; i++){
    unsigned long long result = part1[i] & part2[i];
    if(result != 0)
      return true;
  }
  return false;
}

unsigned long long* placeOnImage(unsigned long long OGIMG[4], word block, short pos[2]){
  short maxX = pos[0]+4;
  short maxY = pos[1]+4;
  if(maxX > 16 || maxY > 16 || pos[0] < 0 || pos[1] < 0)
    return 0;//block off screen
  for(int x = pos[0]; x < maxX; x++){
    for(int y = pos[1]; y < maxY; y++){
      short arrayX = 0;
      short arrayY = 0;
      if (x >= 8){
        x -= 8;
        arrayX += 1;
      }
      if (y >= 8){
        y -= 8;
        arrayY += 1;
      }
      unsigned long long varToOR = 0;
      short bitIndexToTrue = 0;
      bitIndexToTrue += 8*y;
      bitIndexToTrue += x;
      varToOR = 1 << bitIndexToTrue;
      OGIMG[arrayX+2*arrayY] = OGIMG[arrayX+2*arrayY] | varToOR;
    }
  }
  return OGIMG;
}
