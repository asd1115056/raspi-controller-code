#include <SoftwareSerial.h>   // 引用程式庫
#include <string.h>
int Input = 2;
char data[]="In a series of tweets, Mr Trump said he had been set to meet senior Taliban leaders at Camp David on Sunday.However he cancelled the meeting and called off negotiations after the group admitted to an attack in Kabul that killed a US soldier.US negotiator Zalmay Khalilzad had announced a peace deal in principle with the Taliban on Monday.As part of the proposed deal, the US would withdraw 5,400 troops from Afghanistan within 20 weeks. However Mr Khalilzad said final approval still rested with Mr Trump.The US currently has about 14,000 troops in the country.";

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
  if (s=="test") {
    BT.println(data);
    Serial.println("ok");
    }
  Serial.println(s);
  delay(1);
  }
  
}