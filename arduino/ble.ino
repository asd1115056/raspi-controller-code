#include <SoftwareSerial.h>   // 引用程式庫
#include <string.h>
int Input = 2;
char data[]="[{'subject':'Math','score':80},{'subject':'Math','score':80},{'subject':'Math','score':80},{'subject':'Math','score':80},{'subject':'Math','score':80},{'subject':'Math','score':80},{'subject':'Math','score':80}]";
// 定義連接藍牙模組的序列埠
SoftwareSerial BT(8, 9); // 接收腳, 傳送腳
char val;  // 儲存接收資料的變數
String s;
void setup() {
  Serial.begin(9600);   // 與電腦序列埠連線
  Serial.println("BT is ready!");
  pinMode(2,INPUT);
  //attachInterrupt(0, StateChanged, RISING);
  //BT.setTimeout(1);
  // 設定藍牙模組的連線速率
  // 如果是HC-05，請改成38400
  BT.begin(9600);
}
void StateChanged(){
  if (BT.available()) {
  s = BT.readString();
  Serial.println(s);
  if (s=="t") BT.print("ok");}
  Serial.println("interrupt\n");
  delay(5);
  }


void loop() {
  if (BT.available()) {
  s = BT.readString();
  if (s=="test") {/*
    BT.println("ok");
    Serial.println("ok");*/
      BT.print(data);
      delay(50);
      BT.print("/0");
      delay(50);
    }
  Serial.println(s);
  delay(1);
  }
  
}