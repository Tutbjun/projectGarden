//funktion der danner kalibreringsværdier for sensorer
void kalibrerSensor() {
  delay(1000);
  Serial.println("Giv høj");//beder om lys værdi
  int datHigh[sensorAntal];
  while (digitalRead(knapPin) == LOW) {//skriver konstant sensorværdier ind i arrayet indtil knappen bliver trykket ned igen
    digitalWrite(ledPin, HIGH);//blinker LED indtil data er modtaget
    delay(20);
    digitalWrite(ledPin, LOW);
    delay(20);
    for (int i = 0; i < sensorAntal; i++)//skriver data ind i array
      datHigh[i] = analogRead(sensorPins[i]);
  }
  delay(1000);
  Serial.println("Giv Lav");//beder om mørk værdi
  int datLow[sensorAntal];
  while (digitalRead(knapPin) == LOW) {//skriver konstant sensorværdier ind i arrayet indtil knappen bliver trykket ned igen
    digitalWrite(ledPin, HIGH);//blinker LED indtil data er modtaget
    delay(20);
    digitalWrite(ledPin, LOW);
    delay(20);
    for (int i = 0; i < sensorAntal; i++)//skriver data ind i array
      datLow[i] = analogRead(sensorPins[i]);
  }

  //finder sensorernes hædningskoeficienter
  for (int i = 0; i < sensorAntal; i++)
    sensorAer[i] = datHigh[i] - datLow[i];
  //inverterer den fundne koeficient så det kan bruges til at normalisere data
  for (int i = 0; i < sensorAntal; i++) {
    sensorAer[i] /= 1023;
    sensorAer[i] = pow(sensorAer[i], -1);
  }
  //laver et inverteret serie a y-forskydninger til at normalisere data
  for (int i = 0; i < sensorAntal; i++) {
    sensorBer[i] = -datLow[i];
  }

  //printer fundne b-værdier
  Serial.println("Sensor B'er:");
  delay(100);
  for (int i = 0; i < sensorAntal; i++) {
    Serial.println(sensorBer[i]);
    delay(100);
  }

  //printer fundne a-værdier
  Serial.println("Sensor A'er:");
  for (int i = 0; i < sensorAntal; i++) {
    Serial.println(sensorAer[i]);
    delay(100);
  }

  //komunikerer at den er kalibreret
  digitalWrite(ledPin, HIGH);
  delay(1000);
  digitalWrite(ledPin, LOW);
}
