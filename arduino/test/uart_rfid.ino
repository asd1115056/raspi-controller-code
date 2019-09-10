#include <SoftwareSerial.h>
#include <string.h>

SoftwareSerial rfid(8, 9); // Duemilanove

int i = 0;
unsigned char searchCMD[5] = {0xAA, 0xBB, 0x02, 0x20, 0x22};
unsigned char searchRES[10];
String s = "";
void setup() {
  Serial.begin(9600);
  Serial.print("ok\n");
  rfid.begin(19200);
  gettag();
  Serial.print(s);
}
void gettag() {
  s = "";
  rfid.write(searchCMD, 5);
  delay(120);
  if (rfid.available()) {
    rfid.readBytes(searchRES, 10);
    if (searchRES[0] == 0xaa && searchRES[3] != 0xdf) {
      for (int i = 0; i < 9; i++) {
        s += String(searchRES[i], HEX);
      }
      s=s.substring(7,15);
    }
  }
}
void loop() {}