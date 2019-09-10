#include <SoftwareSerial.h>
#include <string.h>

int BT_statue_pin = 2;
SoftwareSerial BT(8, 9); // rx,tx
String BT_readString;

String BT_readString_Part1;
String BT_readString_Part2;
String BT_readString_Part3; // 儲存接收資料的變數
String test_message1 = "job 22bb336b 099";
String test_message2 = "upl"; // upload data
String test_message3 = "add"; // add new Tag

// char sr[];

void setup() {
  Serial.begin(9600); // 與電腦序列埠連線
  Serial.println("BT is ready!");
  pinMode(BT_statue_pin, INPUT);
  BT.begin(9600);
}
/*
void BT_interrupt() {
  
  Serial.println("interrupt");
}*/
void loop() {

  if (BT.available()) {
    BT_readString = BT.readString();
    Serial.println(BT_readString);
    BT.print("ok");

    BT_readString_Part1 = BT_readString.substring(0, 3);
    BT_readString_Part2 = BT_readString.substring(4, 12);
    BT_readString_Part3 = BT_readString.substring(13, 16);

    if (BT_readString_Part1 == "job") {
      bool state = true;
      while (state) {
        Serial.println("job");
        state = false;
      }
    }
    if (BT_readString_Part1 == "upl") {
      Serial.println("upl");    
    }
    if (BT_readString_Part1 == "add") {
      Serial.println("add");
    }
  }
  else{
    Serial.println("hi");



  }
}
