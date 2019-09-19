#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <RtcDS3231.h>
#include <SD.h>
#include <SPI.h>
#include <Time.h>
#include <Wire.h> // must be included here so that Arduino library object file references work
#include <string.h>

RtcDS3231<TwoWire> Rtc(Wire);

#define DHTPIN 22
#define DHTTYPE DHT11
DHT_Unified dht(DHTPIN, DHTTYPE);

#define RtcSquareWavePin 2       // Mega2560
#define RtcSquareWaveInterrupt 0 // Mega2560

#define BTPin 3       // Mega2560
#define BTInterrupt 1 // Mega2560

#define chipSelect 53

#define location_code "A"
#define RFID_statue_pin 4

volatile uint16_t interuptCount = 0;
volatile bool interuptFlag = false;
unsigned char searchCMD[5] = {0xAA, 0xBB, 0x02, 0x20, 0x22};
unsigned char searchRES[10];

String TAG = "";
String BT_readString;
String test_message1 = "job 22bb336b 099";
String test_message2 = "upl"; // upload data
String test_message3 = "add"; // add new Tag
bool BT_statue = false;
bool RFID_statue = false;

File myFile;
Sd2Card card;
SdVolume volume;
SdFile root;

void RTC() {
  pinMode(RtcSquareWavePin, INPUT_PULLUP);
  Rtc.Begin();
  RtcDateTime compiled = RtcDateTime(__DATE__, __TIME__);

  if (!Rtc.IsDateTimeValid()) {
    if (Rtc.LastError() != 0) {
      // we have a communications error
      // see https://www.arduino.cc/en/Reference/WireEndTransmission for
      // what the number means
      Serial.print("RTC communications error = ");
      Serial.println(Rtc.LastError());
    } else {
      Serial.println("RTC lost confidence in the DateTime!");
      Rtc.SetDateTime(compiled);
    }
  }

  if (!Rtc.GetIsRunning()) {
    Serial.println("RTC was not actively running, starting now");
    Rtc.SetIsRunning(true);
  }

  RtcDateTime now = Rtc.GetDateTime();
  if (now < compiled) {
    Serial.println("RTC is older than compile time!  (Updating DateTime)");
    Rtc.SetDateTime(compiled);
  }

  Rtc.Enable32kHzPin(false);
  Rtc.SetSquareWavePin(DS3231SquareWavePin_ModeAlarmBoth);

  // Alarm 2 set to trigger at the top of the minute
  DS3231AlarmTwo alarm2(0, 0, 0, DS3231AlarmTwoControl_OncePerMinute);
  Rtc.SetAlarmTwo(alarm2);

  // throw away any old alarm state before we ran
  Rtc.LatchAlarmsTriggeredFlags();

  // setup external interupt
  attachInterrupt(RtcSquareWaveInterrupt, InteruptServiceRoutine, FALLING);
  Serial.println("initializing RTC...Success!");
}
void SD1() {
  Serial.print("initializing SD card...");
  if (!SD.begin(53)) {
    Serial.println("Fail!");
    return;
  }
  Serial.println("Success!");
}
void setup() {
  Serial.begin(115200);
  Serial1.begin(115200);
  Serial2.begin(19200);

  SD1();
  dht.begin();
  RTC();
  pinMode(BTPin, INPUT_PULLUP);
  pinMode(RFID_statue_pin, INPUT);
  attachInterrupt(BTInterrupt, BTRoutine, RISING);
  Serial.println("initializing RFID...Success!");
  Serial.println("initializing BT...Success!");
  Serial.println("initializing DHT...Success!");
  delay(100);
}
void BTRoutine() {
  //
  BT_statue = true;
}
void InteruptServiceRoutine() {
  // since this interupted any other running code,
  // don't do anything that takes long and especially avoid
  // any communications calls within this routine
  interuptCount++;
  interuptFlag = true;
}
void loop() {
  sensors_event_t event;
  if (BT_statue) {
    // Serial.println("HIGH");
    Serial.println("=================== Task =======================");
    if (Serial1.available()) {
      BT_readString = Serial1.readString();
      Serial.print("BT:Pi Command: ");
      Serial.println(BT_readString);
      // Serial1.print("ok");
      /*
      BT_readString_Part1 = BT_readString.substring(0, 3);
      BT_readString_Part2 = BT_readString.substring(4, 12);
      BT_readString_Part3 = BT_readString.substring(13, 16);
      */
      if (BT_readString == "test") {
        Serial1.print("ok");
      }
      if (BT_readString.substring(0, 3) == "job") {
        bool state = true;
        while (state) {
          TAG = "";
          Serial2.write(searchCMD, 5);
          delay(120);
          if (Serial2.available()) {
            Serial2.readBytes(searchRES, 10);
            if (searchRES[0] == 0xaa && searchRES[3] != 0xdf) {
              for (int i = 0; i < 9; i++) {
                TAG += String(searchRES[i], HEX);
              }
              if (TAG.substring(7, 15) == BT_readString.substring(4, 12)) {
                state = false;
              }
            }
          }
        }
        //倒飼料
      }
      if (BT_readString.substring(0, 3) == "upp") {
        //讀取sd 回傳
        Serial.println("Send pet data by BLE");
        RtcDateTime now = Rtc.GetDateTime();
        printDateTime(now);
        myFile = SD.open("pet.txt");
        if (myFile) {
          while (myFile.available()) {
            Serial1.write(myFile.read());
          }
          myFile.close();
          delay(50);
          Serial.println("done");
        } else {
          Serial.println("error opening file");
        }
      }
      if (BT_readString.substring(0, 3) == "upe") {
        //讀取sd 回傳
        Serial.println("Send env data by BLE");
        RtcDateTime now = Rtc.GetDateTime();
        printDateTime(now);
        myFile = SD.open("env.txt");
        if (myFile) {
          while (myFile.available()) {
            Serial1.write(myFile.read());
          }
          myFile.close();
          delay(50);
          Serial.println("done");
        } else {
          Serial.println("error opening file");
        }
      }
      if (BT_readString.substring(0, 3) == "dlp" ||
          BT_readString.substring(0, 3) == "dle") {
        //讀取sd 回傳
        Serial.println("Del file");
        RtcDateTime now = Rtc.GetDateTime();
        printDateTime(now);
        Serial.print("Del: ");
        if (BT_readString.substring(0, 3) == "dlp") {
          SD.remove("pet.txt");
          Serial.print("pet.txt");
        }
        if (BT_readString.substring(0, 3) == "dle") {
          SD.remove("env.txt");
          Serial.print("env.txt");
        }
        Serial.println();
        Serial1.print("Del:ok");
        Serial.println("done");
      }
    }
    BT_statue = false;
    Serial.println("================= Finished =====================");
    Serial.println();
  }
  if (!BT_statue) {
    if (RFID_statue) {
      Serial.println("=================== Task =======================");
      Serial.println("RFID:Record pet data");
      RtcDateTime now = Rtc.GetDateTime();
      printDateTime(now);
      TAG = "";
      Serial2.write(searchCMD, 5);
      delay(120);
      if (Serial2.available()) {
        Serial2.readBytes(searchRES, 10);
        if (searchRES[0] == 0xaa && searchRES[3] != 0xdf) {
          for (int i = 0; i < 9; i++) {
            TAG += String(searchRES[i], HEX);
          }
          TAG = TAG.substring(7, 15);
          Serial.print("Tag: ");
          Serial.println(TAG);
        }
      }
      RFID_statue = false;
      Serial.println("================= Finished =====================");
      Serial.println();
    }
    if (Alarmed() && interuptCount % 3 == 0) {
      //定時紀錄溫溼度 存入sd
      sensors_event_t event;
      Serial.println("=================== Task =======================");
      Serial.println("Alarm:Record env data");
      myFile = SD.open("env.txt", FILE_WRITE);
      if (myFile) {
        myFile.print("E");
        myFile.print(location_code);

        RtcDateTime now = Rtc.GetDateTime();
        myFile.print(now);
        printDateTime(now);

        dht.temperature().getEvent(&event);
        myFile.print(event.temperature);
        Serial.print(F("Temperature: "));
        Serial.print(event.temperature);
        Serial.print(F("°C"));

        Serial.println(" ");

        dht.humidity().getEvent(&event);
        myFile.print(event.relative_humidity);
        Serial.print(F("Humidity: "));
        Serial.print(event.relative_humidity);
        Serial.println(F("%"));

        delay(100);

        myFile.println();
        myFile.close();
        Serial.println("done");
      } else {
        Serial.println("error opening file");
      }
      Serial.println("================= Finished =====================");
      Serial.println();
    }
    if (interuptCount > 8) {
      interuptCount = 0;
    }
  }
  if (digitalRead(RFID_statue_pin) == LOW) {
    // J1-7 有卡 輸出低電位
    RFID_statue = true;
  }
}

bool Alarmed() {
  bool wasAlarmed = false;
  if (interuptFlag) // check our flag that gets sets in the interupt
  {
    wasAlarmed = true;
    interuptFlag = false; // reset the flag

    // this gives us which alarms triggered and
    // then allows for others to trigger again
    DS3231AlarmFlag flag = Rtc.LatchAlarmsTriggeredFlags();
    /*
        if (flag & DS3231AlarmFlag_Alarm2)
        {
            Serial.println("alarm two triggered");
        }
        */
  }
  return wasAlarmed;
}
#define countof(a) (sizeof(a) / sizeof(a[0]))

void printDateTime(const RtcDateTime &dt) {
  char datestring[20];

  snprintf_P(datestring, countof(datestring),
             PSTR("%04u-%02u-%02u %02u:%02u:%02u"), dt.Year(), dt.Month(),
             dt.Day(), dt.Hour(), dt.Minute(), dt.Second());
  Serial.println(datestring);
}