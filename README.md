# mBot Maszk Érzékelés
## Versenyfeladat: [Tekintsd Meg Itt!](https://www.inf.u-szeged.hu/sziiv)

# Mire is jó a projekt?
## Sokat gondolkoztunk, milyen ötlettel álljunk elő a versenyre, de mvégül napjaink egyik legnagyobb veszélyforrásának megoldására akartunk megoldást találni. A [Covid-19](https://hu.wikipedia.org/wiki/Covid19) már mindenki számára ismert, mint ahogy a maszkhordási kötelezettség is! Bár a szabályokon enyhítettek, a kötelezettség betartása, ezzel együtt embertársaink védelme fontos számunkra! Ezért alkottunk egy olyan rendszert, mely felsimeri, ha az illető **NEM VISEL MASZKOT**, ezenfelül figyelmezteti a személyt, a szabály betartásának fontosságáról. Mindezt a robot bármilyen adatgyűjtés, képmentés, képtárolás (mint kódszinten, mint fájlszinten) nélkül teszi. Természetesen, ha az egység egy helyben állna, nem lenne biztos a maszkfelvétel. Ebben van segítségünkre a [Makeblock Bot (mBot)](https://www.makeblock.com/steam-kits/mbot) robot kisautó. Programját módosítva képesek vagyunk a szenzorok által kinyert adatok alapján egy önjáró robottá alakítani. Képes falakat kikerülni, valamint a lépcsőkről sem gurul le. A robot ideális kisebb közösségek tereibe, iskolákba, munkahelyekre, egyéb intézéményekbe. A következő leírásban a robot pomntos felépítését, követelményeit, működését olvashatjuk!

<br><br>

# Működés
## A program működését 3 fő részre bontottuk:
- ## Mozgás
- ## Maszk Érzékelés
- ## Figyelmeztetés

## Mozgás:
### Az alap mozgás kód jó kezdet volt ahhoz, hogy tudjuk milyen kódsor(bitearray) mit vezérel. Ebből kidolgozva a szenzorok adatait felhasználva alkottuk meg a robot önjáró mozgását. Korai lenne mesterséges inteligenciának nevezni, hiszen nem "jegyzi" meg, hogy hol vannak lépcsők, falak, de kikerülni azokat szinte minden esetben kiekrüli.

## Maszk Érzékelés:
### A maszk érzékelés is két részre bomlik (tensorflow, keras). Első részben a kamera képét, azon belül minden egyes képkockát elemzünk. Ha nem találunk rajta arcot, továbblépünk a következő képkockára. Ha viszont a program felismer egy arcot, jön a második része a programnak. Ellenőrizzük, hogy az illető arcát takarja-e maszk. Ha igen, a program szintén a következő képkockát figyeli.

## Figyelmeztetés:
### Ha az adott képkockában lévő arcot nem takarta maszk, a rendszer, egy személyre szabható [figyelmezetéseket](https://github.com/tcgmilan/mbot-mask-detection/blob/master/figyelmeztetesek.txt) tartalmazó listából véletlenszerűen választ egy üzenetet, majd felolvassa az illetőnek. Az ezután következő késleltetés is állítható, amely mindössze annyit határoz meg, mennyit várjon a robot a következő ellenőrzés előtt. Célszerű egy olyan időt meghatározni, amely elegendő egy maszk elővételéhez, felvételéhez. Ellenkező esetben a program többször is felszólithatja a célszemélyt.

<br><br>

# Felépítés
- ### Raspberry PI 3B (Raspberryi OS - Version 11, Bullseye)
- ### Kamera (Microsoft, 480p, 30fps)
- ### Makeblock mBot ([Módosított firmware](https://github.com/tcgmilan/mbot-mask-detection/tree/dev/mbot_firmware))
- ### Akkumulátorok (2 cellás, 8000 mAh (2x4000 mAh))

<br><br>

# Működés
## A robot a bekapcsolást követően azonnal üzembe helyezhető, konfigurálás nélkül, **AZONBAN AJÁNLOTT A BEÁLLÍTÁSOKAT SZEMÉLYRE SZABNI!**

<br><br>

# Követelmények
- ### python 3.10.x
- ### numpy 1.20.0
- ### tensorflow 2.8.0 **
- ### keras
- ### pyttsx3
- ### opencv
- ### h5py
- ### scipy

<br><br>

# Haladóknak
## Tensorflow:
### A tensorflow telepítése körülményesebb, ennek leírását itt találhatjátok:
```bash
$ pip3 install -r requirements.txt

$ git clone https://github.com/Qengineering/Tensorflow-io.git

$ cd Tensorflow-io

$ sudo -H pip3 install tensorflow_io_gcs_filesystem-0.23.1-cp39-cp39-linux_aarch64.whl

$ cd ~

$ sudo -H pip3 install gdown

$ gdown https://drive.google.com/uc?id=1YpxNubmEL_4EgTrVMu-kYyzAbtyLis29

$ sudo -H pip3 install tensorflow-2.8.0-cp39-cp39-linux_aarch64.whl
```
