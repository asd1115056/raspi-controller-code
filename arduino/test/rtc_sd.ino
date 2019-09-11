#include <RtcDS1307.h>
#include <SD.h>
#include <SPI.h>
#include <SoftwareSerial.h> // 引用程式庫
#include <Time.h>
#include <Wire.h> // must be included here so that Arduino library object file references work
#include <string.h>

RtcDS1307<TwoWire> Rtc(Wire);
File dataFile;
const int chipSelect = 4;
SoftwareSerial BT(8, 9);
char datestring[20] = {0};
String s;

void setup() {
  Serial.begin(9600);
  BT.begin(9600);
  Rtc.Begin();
  pinMode(A0, OUTPUT);
  digitalWrite(A0, HIGH);

  Serial.print("initializing SD card...");

  if (!SD.begin(4)) {
    Serial.println("Fail!");
    return;
  }
  Serial.println("initialized done");
  delay(400);
  dataFile = SD.open("temp.txt", FILE_WRITE);
  if (dataFile) {
    dataFile.println("Date_Time,temp(C)");
    dataFile.close();
  } else {
    Serial.println("\n open file error ");
  }
}

void loop() {
  /*
    Serial.print("Pls wait.......");
    Serial.println();
    delay(1000);
    dataFile = SD.open("temp.csv", FILE_WRITE);
    if (dataFile) {
      Serial.println("Writing..");
      RtcDateTime now = Rtc.GetDateTime();
      printDateTime(now);
      dataFile.print(datestring);
      dataFile.print(",");
      dataFile.println("25");
      delay(10000);
      dataFile.close();
      Serial.println("done");
    } else {
      Serial.println("error opening test.txt");
    }
    */

  if (BT.available()) {
    s = BT.readString();
    if (s == "test") {
      dataFile = SD.open("temp.txt");
      if (dataFile) {
        Serial.println("temp.txt:");

        // read from the file until there's nothing else in it:
        while (dataFile.available()) {
          BT.write(dataFile.read());
        }
        // close the file:
        dataFile.close();
      } else {
        // if the file didn't open, print an error:
        Serial.println("error opening test.txt");
      }
      //BT.println(data);
      Serial.println("ok");
    }
    Serial.println(s);
    delay(10);
  }
}
#define countof(a) (sizeof(a) / sizeof(a[0]))
void printDateTime(const RtcDateTime &dt) {
  datestring[20] = {0};

  snprintf_P(datestring, countof(datestring),
             PSTR("%04u-%02u-%02u %02u:%02u:%02u"), dt.Year(), dt.Month(),
             dt.Day(), dt.Hour(), dt.Minute(), dt.Second());
  Serial.print(datestring);
}