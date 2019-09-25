#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <HX711.h>
#include <RtcDS3231.h>
#include <SD.h>
#include <SPI.h>
#include <Stepper.h>
#include <Time.h>
#include <Wire.h> // must be included here so that Arduino library object file references work
#include <string.h>

#define STEPS 100 //設置步進馬達旋轉一圈是多少步
Stepper stepper(STEPS, 9, 10, 11,
                12); //設置步進馬達的步數和引腳(Pin9, Pin10, Pin11, Pin12)

RtcDS3231<TwoWire> Rtc(Wire);

const int LOADCELL_DOUT_PIN = 5;
const int LOADCELL_SCK_PIN = 6;
HX711 scale;
#define ratio 400.352

#define DHTPIN 22
#define DHTTYPE DHT11
DHT_Unified dht(DHTPIN, DHTTYPE);

#define RtcSquareWavePin 2       // Mega2560
#define RtcSquareWaveInterrupt 0 // Mega2560

#define BT Serial2
#define BTPin 3       // Mega2560
#define BTInterrupt 1 // Mega2560

#define WaterFlowpin 19      // Mega2560
#define WaterFlowInterrupt 4 // Mega2560
#define chipSelect 53

#define RFID Serial3
#define location_code "A"
#define RFID_statue_pin 4

volatile uint16_t interuptCount = 0;
volatile bool interuptFlag = false;
unsigned char searchCMD[5] = {0xAA, 0xBB, 0x02, 0x20, 0x22};
unsigned char searchRES[10];

String TAG = "";
String BT_readString = "";
// String test_message1 = "job22bb336b099.9";
bool BT_statue = false;
bool RFID_statue = false;

volatile float waterFlow;
float FG = 000.0, SG = 000.0, DF = 000.0;
File myFile;
Sd2Card card;
SdVolume volume;
SdFile root;

const int buzzerpin = 8; // 用Pin8 輸出方波至蜂鳴器

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
  Serial.println("RTC...Success!");
}
void SD1() {
  Serial.print("SD card...");
  if (!SD.begin(53)) {
    Serial.println("Fail!");
    return;
  }
  // SD.remove("pet.txt");
  // SD.remove("env.txt");
  Serial.println("Success!");
}
void HX7111() {
  Serial.println("HX711...Success!");
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(ratio); // this value is obtained by calibrating the scale
                          // with known weights; see the README for details
  scale.tare();           // reset the scale to 0
}
void setup() {
  Serial.begin(115200);
  BT.begin(115200);
  RFID.begin(19200);
  Serial.println("=============== Initializing ===================");
  SD1();
  dht.begin();
  HX7111();
  RTC();
  pinMode(BTPin, INPUT_PULLUP);
  pinMode(RFID_statue_pin, INPUT);
  pinMode(WaterFlowpin, INPUT);
  attachInterrupt(BTInterrupt, BTRoutine, RISING);
  attachInterrupt(WaterFlowInterrupt, WaterFlowpulse, RISING);
  pinMode(buzzerpin, OUTPUT);
  stepper.setSpeed(STEPS);
  Serial.println("RFID...Success!");
  Serial.println("BLE...Success!");
  Serial.println("DHT11...Success!");
  Serial.println("================= Finished =====================");
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
void WaterFlowpulse() // measure the quantity of square wave
{
  waterFlow += 1000.0 / 5880.0;
}
void loop() {
  sensors_event_t event;
  if (BT_statue) {
    // Serial.println("HIGH");
    Serial.println("=================== Task =======================");
    if (BT.available()) {
      BT_readString = BT.readString();
      Serial.print("BT:Pi Command: ");
      Serial.println(BT_readString);
      // Serial.println(BT_readString.substring(3, 11));
      // Serial.println(BT_readString.substring(11, 17));
      // BT.print("ok");
      /*
      BT_readString_Part1 = BT_readString.substring(0, 3);
      BT_readString_Part2 = BT_readString.substring(3, 11);
      BT_readString_Part3 = BT_readString.substring(11, 17);
      */
      if (BT_readString == "test") {
        BT.print("ok");
      }
      if (BT_readString.substring(0, 3) == "job") {
        BT.print("ok");
        Serial.println("Job feed");
        Serial.println("Search Tag...");
        RtcDateTime now = Rtc.GetDateTime();
        printDateTime(now);
        bool state = true;
        while (state) {
          tone(buzzerpin, 1000, 100);
          TAG = "";
          RFID.write(searchCMD, 5);
          delay(120);
          if (RFID.available()) {
            RFID.readBytes(searchRES, 10);
            if (searchRES[0] == 0xaa && searchRES[3] != 0xdf) {
              for (int i = 0; i < 9; i++) {
                TAG += String(searchRES[i], HEX);
              }
              if (TAG.substring(7, 15) == BT_readString.substring(3, 11)) {
                float total = 0, j1 = 0, j2 = 0;
                Serial.print("Tag: ");
                Serial.println(TAG.substring(7, 15));

                scale.power_up();
                j1 = scale.get_units(5);
                Serial.print("Frist weight: ");
                Serial.println(j1);

                while (1) {
                  //倒飼料

                  stepper.step(36);

                  // scale.power_up();
                  j2 = scale.get_units(5);
                  // scale.power_down();
                  Serial.print("Weight: ");
                  Serial.println(j2);

                  total = j2 - j1;
                  Serial.print("DF weight: ");
                  Serial.println(total);
                  if (total >= BT_readString.substring(11, 17).toFloat()) {
                    break;
                  }
                }
                state = false;
                scale.power_down();
              }
            }
          }
        }
      }
      if (BT_readString.substring(0, 3) == "upp") {
        //讀取sd 回傳
        Serial.println("Send pet data by BLE");
        RtcDateTime now = Rtc.GetDateTime();
        printDateTime(now);
        myFile = SD.open("pet.txt");
        if (myFile) {
          while (myFile.available()) {
            BT.write(myFile.read());
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
            BT.write(myFile.read());
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
        BT.print("Del:ok");
        Serial.println("done");
      }
    }
    BT_statue = false;
    Serial.println("================= Finished =====================");
    Serial.println();
  }
  if (!BT_statue) {
    if (RFID_statue) {
      TAG = "";
      RFID.write(searchCMD, 5);
      delay(120);
      if (RFID.available()) {
        RFID.readBytes(searchRES, 10);
        if (searchRES[0] == 0xaa && searchRES[3] != 0xdf) {
          for (int i = 0; i < 9; i++) {
            TAG += String(searchRES[i], HEX);
          }
          TAG = TAG.substring(7, 15);
          if (TAG != "") {
            Serial.println("=================== Task =======================");
            Serial.println("RFID:Record pet data");
            myFile = SD.open("pet.txt", FILE_WRITE);
            if (myFile) {
              myFile.print("P");
              myFile.print(location_code);
              Serial.print("Tag: ");
              Serial.println(TAG);
              myFile.print(TAG);

              RtcDateTime now = Rtc.GetDateTime();
              printDateTime(now);
              myFile.print(now);

              scale.power_up();
              FG = scale.get_units(10);
              Serial.print("First: ");
              Serial.print(FG);
              Serial.print(" g");
              Serial.println();
              scale.power_down();

              delay(9880);

              scale.power_up();
              SG = scale.get_units(10);
              Serial.print("Second: ");
              Serial.print(SG);
              Serial.print(" g");
              Serial.println();
              scale.power_down();
              if (SG > FG) {
                DF = SG - FG;
              }
              if (SG <= FG) {
                DF = FG - SG;
              }
              if (DF <= 0.9) {
                DF = 0.0;
              }
              String temp1 = "";
              if (DF >= 0 && DF < 10) {
                temp1 = String("") + "00" + DF;
              }
              if (DF >= 10 && DF < 100) {
                temp1 = String("") + "0" + DF;
              }

              Serial.print("Difference: ");
              Serial.print(temp1);
              Serial.print(" g");
              Serial.println();
              myFile.print(temp1);

              String temp2 = "";
              if (waterFlow >= 0 && waterFlow < 10) {
                temp2 = String("") + "00" + waterFlow;
              }
              if (waterFlow >= 10 && waterFlow < 100) {
                temp2 = String("") + "0" + waterFlow;
              }

              Serial.print("waterFlow: ");
              Serial.print(temp2);
              Serial.println(" mL");
              myFile.print(temp2);
              myFile.println();

              myFile.close();
              Serial.println("done");
            } else {
              Serial.println("error opening file");
            }
            Serial.println("================= Finished =====================");
            Serial.println();
          }
        }
      }
      waterFlow = 000.00;
      FG = 000.0, SG = 000.0, DF = 000.0;
      RFID_statue = false;
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

        Serial.print(F("Temperature: "));
        if (!isnan(event.relative_humidity)) {
          Serial.print(event.temperature);
          myFile.print(event.temperature);
          Serial.println(F("°C"));
        } else {
          Serial.println("error !");
        }

        dht.humidity().getEvent(&event);
        Serial.print(F("Humidity: "));
        if (!isnan(event.relative_humidity)) {
          Serial.print(event.relative_humidity);
          myFile.print(event.relative_humidity);
          Serial.println(F("%"));
        } else {
          Serial.println("error !");
        }

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