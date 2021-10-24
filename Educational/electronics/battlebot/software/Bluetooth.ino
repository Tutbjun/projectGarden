int integraleVinkel = 0;//integralet af vinklen siden programstart

//aflæser bluetooth seriel og laver commands på basis af det
void bluetooth_(){
  if (bluetooth.available()) {
    data = bluetooth.read();//læser input
    //Serial.println(data); 
    if(data != '/'){//hvis det ikke er en specielkommando
      if (data == 'S'){//skyder
        kaShoot();
      }
      if (data == 'H'){//stopper
        stop_();
      }
      else if (data == 'F'){//kører fremad
        foward();
      }
      else if (data == 'R'){//drejer til højre
        turnRight();
      }
      else if (data == 'L'){//drejer til venstre
        turnLeft();
      }
      else if (data == 'B'){//kører baglæns
        backward();
      }
      else if (data == 'O'){//tænder auto
        pidON = true;
        integraleVinkel = 0;
      }
      else if (data == 'o'){//slukker auto og stopper motere
        pidON = false;
        stop_();
      }
      else if (data == 'd' || data == 'p' || data == 'i' || data == 'v'){//hvis det er en af variabeljusteringsværdier
        char toBeSet = data;
        while(!bluetooth.available()){//efter den har modtaget hvilken værdi der skal justeres, så venter den på dataet
          digitalWrite(ledPin, HIGH);
          delay(150);
          digitalWrite(ledPin, LOW);
          delay(150);
        }
        String inputData = "";
        while(bluetooth.available()){//nedskriver modtaget data i en string
          data = bluetooth.read();
          String dataString = String(data);
          inputData += dataString;
        }
        //konverterer stringen til en float og sætter koeficienterne til inputtet
        if(toBeSet == 'd')
          Kd = inputData.toFloat();
        if(toBeSet == 'p')
          Kp = inputData.toFloat();
        if(toBeSet == 'i')
          Ki = inputData.toFloat()-0.5;
        if(toBeSet == 'v')
          speedVal = inputData.toFloat();
        Serial.print("p:");
        Serial.println(Kp);
        Serial.print("i:");
        Serial.println(Ki);
        Serial.print("d:");
        Serial.println(Kd);
      }
    }
    //hvis den modtager en speciel kommando. dvs hvis den modtager /[kommando]
    else if (data == '/'){
      String inputData = "";
      while(bluetooth.available()){//laver en string med den samlede kommando
        data = bluetooth.read();
        String dataString = String(data);
        inputData += dataString;
        //Serial.println(inputData);
      }
      if (inputData == "spinbot"){//sætter motorne til at dreje og kører fast på en uendelig løkke
        spinbot();
        while(true){};
      }
      else if(inputData == "360"){ //drejer 360 grader og skyder
        spinbot();
        delay(800);
        stop_();
        kaShoot();
      }
    }
  }
}
