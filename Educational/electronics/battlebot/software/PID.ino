float sensorVinkler[5] = {-820.305,-327.249,4.363,386.416,880.519};//sensorvinkler
float vinkelSerie[2];//serie med flere optagede vinkler så den er mere sikker
long vinkelTidSerie[2];//tidspunkter for vinkelserierne

float vinkelAvg = 0;//gennemsnit af vinkelSerie
long sidstePIDtid; //benyttes til at finde integralet

long kunSortTid = 0;

//returnerer den koeficient som den skal dreje med
int accPID(float dat1[]){
  bool kunSort = true;
  for(int i = 0; i < sensorAntal; i++){
    if(dat1[i] > 50){
      kunSort = false;
    }
  }
  if(kunSort && kunSortTid < millis()-5000){
    kunSortTid = millis();
    stop_();
    delay(200);
    kaShoot();
    delay(200);
    return 0;
  }
  
  //flytter alle værdier i vinkelserien og vinkeltidspunkterserien en index
  for(int i = sizeof(vinkelSerie)/4-1; i > 0 ; i--){
    vinkelSerie[i] = vinkelSerie[i-1];
    vinkelTidSerie[i] = vinkelTidSerie[i-1];
  }
  vinkelSerie[0] = findVinkel(dat1);//sætter ny vinkel ind i vinkelserie

  vinkelAvg = 0;//nulstiller nuværende vinkel
  //laver gennemsnit af vinkelserien
  for (int i = 0; i < sizeof(vinkelSerie)/4; i++)
    vinkelAvg += vinkelSerie[i];
  vinkelAvg /= sizeof(vinkelSerie)/4;
  
  integraleVinkel += (float)(millis()-sidstePIDtid) * vinkelAvg;//løbende summering for at finde integralet
  sidstePIDtid = millis();

  vinkelTidSerie[0] = millis();//sætter den nyeste tidsoptagelse for vinkeltidserie
  float vinkelDiff = findHastighed();//finder differentialet, altså vinkelhastigheden
  Serial.println("ree");
  Serial.println(vinkelAvg);
  Serial.println(integraleVinkel);
  Serial.println(vinkelDiff);
  int PIDacc = findPIDacc(vinkelAvg, integraleVinkel, vinkelDiff);//laver sidste udregning for at at komme til drejekoeficienten
  return PIDacc;
}

//bruger de satte konstanter og bruger PID formel til at finde acceleration
int findPIDacc(float vinkel, float iVinkel, float diff){
  float acc = Ki * iVinkel/10 + Kp * vinkel/10 + Kd * diff;
  return (int)acc;
}

//returnerer vinkelhastighed i 1000*radianer/ms
float findHastighed(){
  //laver en serie af differentialer imellem hver aflæste vinkel
  float hastighedSerie[sizeof(vinkelSerie)/4-1];
  for(int i = 0; i < sizeof(vinkelSerie)/4-1; i++){
    float dTheta = vinkelSerie[i]-vinkelSerie[i+1];
    float dT = vinkelTidSerie[i]-vinkelTidSerie[i+1];
    hastighedSerie[i] = dTheta / dT;
  }
  //returnerer gennemsnittet af alle differentialer
  float hastighedSerieSum = 0;
  for(int i = 0; i < sizeof(hastighedSerie)/4; i++)
    hastighedSerieSum += hastighedSerie[i];
  return hastighedSerieSum / sizeof(hastighedSerie)/4 * 1000;
}

//returnerer en vinkel i 1000*radianer
float findVinkel(float dat2[]){
  //ud fra de kalibrerede sensordata finder den gennemsnitsvinklen for de sensorer der læser sort
  float sumVinkler = 0;
  float sumData = 0;
  for(int i = 0; i < sensorAntal; i++){
    sumVinkler += (1000-dat2[i]) * sensorVinkler[i];
    sumData += dat2[i];
  }
  return sumVinkler / sumData;
}
