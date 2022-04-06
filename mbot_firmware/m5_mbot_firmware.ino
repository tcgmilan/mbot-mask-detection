 /*************************************************************************
m5 masKey - mBot firmware
Ez a firmware az mBot gyári firmwarét felhasználva készült, az alábbi módosításokat alkalmazva:
 - az automatikus mozgást továbbfejlesztettük, a feladathoz megfelelőbb mozgásformákat alkalmaztunk (pl. a robot immáron képes tolatni, könnyebben kikeveredik egy szorult helyzetből)
 - kiegészítettük a gyári funkciókat: leesésérzékeléssel láttuk el a mozgatómechanizmust, így egy lépcső sem jelent gondot a robotnak
 - eltávolítottuk a kódból a számunkra felesleges részt, ezzel átláthatóbbá téve a működést és csökkentve a memóriahasználatot
A forrás elérhetősége: https://github.com/Makeblock-official/Makeblock-Libraries
**************************************************************************/ 

 /**A kód elején importáljuk az Arduino illetve az MBlock szükséges könyvtárait,
majd az ezen könyvtárak által kezelhető hardverelemek elérhetőségét (portot, csatlakozást) is megadjuk.
MeUltrasonicSensor a távolságérzékelő, a MeLineFollower pedig a talajérzékelést látja el. 
A két motor, illetve egy általános eszköz (generalDevice) nevű változót is találunk itt, 
ami az összes érzékelőre jellemző feladatokat általánosítja,
(portot, illetve értéket kérünk le vele az aktuális szenzortól). 
A MeBuzzer pedig a beépített berregőt vezérli, melynek segítségével az eszköz bekapcsolását jelezzük.
**/
#include <Wire.h>
#include <SoftwareSerial.h>
#include <MeMCore.h>

MeUltrasonicSensor ultr(PORT_3);
MeLineFollower line(PORT_2);

MeDCMotor MotorL(M1);
MeDCMotor MotorR(M2);
MePort generalDevice;
MeBuzzer buzzer;

//Ezen két változóban adjuk meg a maximális, illetve minimális objektum megközelítési távolságot.
uint8_t maxtav = 30;
uint8_t mintav  = 15;

//Létrehozzuk a memóriában tárolandó elemek tömbjét, és az első elem indexét 0-val tesszük egyenlővé.
char buffer[52];
byte index = 0;

//Meghatározzuk az átlagos mozgási (előrehaladási) sebességet.
int sebesseg = 150;
//Megadjuk a modulok csatlakozási pontját (pin)
#define TAVOLSAGSZENZOR   1
#define TALAJSZENZOR      17
#define MOTOR             10
//Ez a függvény egy megadott index alapján visszaadja a memória tartalmát
unsigned char readBuffer(int16_t index)
{
  return buffer[index]; 
}
/*A különböző mozgások függvényei következnek. 
A MotorL a bal motor, a MotorL a jobb. A run paranccsal vezérelhetjük a motort, melyhez szükség van egy sebesség értékre.
Ha ez a szám az egyik motor esetén negatív, az fordulást eredményez*/
void Elore()
{
  MotorL.run(-sebesseg);
  MotorR.run(sebesseg);
}

void Hatra()
{
  MotorL.run(sebesseg); 
  MotorR.run(-sebesseg);
}

void Balra()
{
  MotorL.run(230);
  MotorR.run(230);
}

void Jobbra()
{
  MotorL.run(-230);
  MotorR.run(-230);
}

void Stop()
{
  MotorL.run(0);
  MotorR.run(0);
}
//A mozgást végző legfontosabb függvény.
void Mozgas()
{
  //Lekérjük a távolságérzékelő szenzor adatait.
  uint8_t d = ultr.distanceCm(70);
  //Generálunk egy véletlen számot 0 és 1 között.
  uint8_t VeletlenSzam = random(2);
//Megvizsgáljuk, hogy a szenzor által visszaadott érték a korábban megadott távolsági határértéken belül, vagy kívül esik.
  if((d > maxtav) || (d == 0))
  {
  //Ha igen, előre haladunk, majd lekérjük a talajérzékelő szenzoradatokat.  
   Elore();
  uint8_t szenzoradat;
  szenzoradat = line.readSensors();
  //A szenzoradatokat külön-külön vizsgáljuk, a jobb, illetve baloldali érzékelő tekintetében.
  switch(szenzoradat)
  {
    //Ha mindkét szenzor távolinak érzékeli a talajt (esés várható), a robot hátrál, majd balra fordul.
    case S1_IN_S2_IN:
      MotorL.run(230); 
      MotorR.run(-230);
      delay(500);
      Balra();
      delay(500);
      break;

    //Ha a baloldali szenzor távolinak érzékeli a talajt (esés várható), a robot hátrál, majd jobbra fordul.
    case S1_IN_S2_OUT:
      MotorL.run(230); 
      MotorR.run(-230);
      delay(500);
      Jobbra();
      delay(500);
      break;
   //Ha a jobboldali szenzor távolinak érzékeli a talajt (esés várható), a robot hátrál, majd balra fordul.
    case S1_OUT_S2_IN:
      MotorL.run(230); 
      MotorR.run(-230);
      delay(500);
      Balra();
      delay(500);
      break;
 //Ha mindkét szenzor úgy érzékeli, hogy a robot a földön tartózkodik, nem avatkozunk közbe.
    case S1_OUT_S2_OUT:
      break;
  }
  }
  //Hogyha a minimális objektum távolság értékét meghaladta, de a maximális közelség értékét még nem érte el a robot, véletlenszerűen hátrál, majd irányt vált.
  else if((d > mintav) && (d < maxtav)) 
  {
    switch (VeletlenSzam)
    {
      case 0:
        Hatra();
        delay(1000);
        Balra();
        delay(2000);
        break;
      case 1:
        Hatra();
        delay(1000);
        Jobbra();
        delay(2000);
        break;
    }
  }
  //Ha már túlléptük a maximális megközelítési távolságot, vagy nem érkezik szenzoradat (minden más esetben), a robot véletlenszerűen próbálkozik jobbra, illetve balra fordulni.
  else
  {
    switch (VeletlenSzam)
    {
      case 0:
        Balra();
        delay(800);
        break;
      case 1:
        Jobbra();
        delay(800);
        break;
    }
  }
  delay(100);
}

//Ez a függvény felel a szenzoradatok kiolvasásáért.
void readSensor(int device)
{
//Létrehozunk egy lebegőpontos szám változót, melyben az értéket tároljuk majd.  
  float value=0.0;
//Létrehozzuk a szenzor elérési pontjait megadó változókat  
  int port,slot,pin;
//Kiolvassuk a memóriából a szenzor portját
  port = readBuffer(6);
//A pint, melyen keresztül az aktuális szenzor elérhető, egyenlővé tesszük a memóriából kiolvasott porthoz tartozó értékkel. 
  pin = port;
//Elágazás, eldöntjük, hogy melyik szenzor adatait kéri le éppen a program
  switch(device)
  {
 /*Mindkét szenzor esetén ellenőrizzük, hogy jó szenzor adatait olvassuk-e be. Ha nem, újra lekérjük a portot.
 Legvégül pedig visszaadjuk az érzékelőkből kinyert értéket.
 */
    case TAVOLSAGSZENZOR:
    {
      if(ultr.getPort() != port)
      {
        ultr.reset(port);
      }
      value = (float)ultr.distanceCm();
    }
    break;
    case TALAJSZENZOR:
    {
      if(generalDevice.getPort() != port)
      {
        generalDevice.reset(port);
        pinMode(generalDevice.pin1(),INPUT);
        pinMode(generalDevice.pin2(),INPUT);
      }
      value = generalDevice.dRead1()*2 + generalDevice.dRead2();
    }
    break;
  }
}
/*A setup függvény az, mely a robot bekapcsolásakor lefut. 
A biztonság kedvéért leállítja a motort, és lejáttsza az indításről visszajelzést adó hangot.
Ezt követően vár 5 másodpercet, mielőtt a robot mozgása megindulna.
 */
void setup()
{
  Stop();
  //A visszajelző hang lejátszása
  buzzer.tone(756, 300);
   //A berregő némítása
  buzzer.noTone();
  delay(5000);
}
/*A void loop az a kódrész, mely a setup függvény lefutását követően folyamatosan fut. Ebben egyetlen dolog történik: meghívjuk a mozgásért felelős, már korábban ismertetett függvényt.*/
void loop()
{
    Mozgas();
}
