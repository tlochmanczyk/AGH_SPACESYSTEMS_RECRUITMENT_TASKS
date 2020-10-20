class MyServo {
  private: 
    int actualPosition;
    int closePosition;
    int openPosition;

  public:
    MyServo(){
      actualPosition = 50;
      closePosition = 100;
      openPosition = 0;      
    }

    MyServo(int openPos, int closePos) {
      actualPosition = 50;
      closePosition = closePos;
      openPosition = openPos;
    }

    int getPosition(){
      return actualPosition;
    }

    bool isOpen(){
      if(actualPosition == openPosition) return true;
      else return false;
    }

    bool isClose(){
      if(actualPosition == closePosition) return true;
      else return false;
    }

    void setPosition(int pos){
      Serial.println("jest");
      actualPosition = pos;
      Serial.println(pos);
    }

    void closeServo(){
      actualPosition = closePosition;
    }

   void openServo(){
      actualPosition = openPosition;
    }

   void setClosePosition(int pos){
      closePosition = pos;
   }

   void setOpenPosition(int pos){
      openPosition = pos;
   }

   String getInfo(){
      String s = "info\n";
      s += actualPosition;
      if(isClose()) s += " closed ";
      else if(isOpen()) s += " open ";
      else s += " normal ";
      s += String(closePosition);
      s += " ";
      s += String(openPosition);
      return s;
   }  
};
///////////////////////////////////////////////////////////////
MyServo servo = MyServo();
///////////////////////////////////////////////////////////////
String actionHandler(String s){
  if(s == "info\n"){
    return servo.getInfo();
  }
  else if(s == "open\n"){
    servo.openServo();
    return s;
  }
  else if(s == "close\n"){
    servo.closeServo();
    return s;
  }
  
  String cmd;
  String arg;
  
  int delim = s.indexOf(' ');
  for(int i=0; i<delim; i++){
    cmd += s[i];
  }
  for(int j=delim+1; j<s.length();j++){
    arg += s[j];
  }

  if(cmd == "pos"){
    servo.setPosition(arg.toInt());
    return s;
  }
  else if(cmd == "setclose"){
    servo.setClosePosition(arg.toInt());
    return s;
  }
  else if(cmd == "setopen"){
    servo.setOpenPosition(arg.toInt());
    return s;
  }
 
}
///////////////////////////////////////////////////////////////
void setup() {
  Serial.begin(9600);
}
///////////////////////////////////////////////////////////////

void loop() {
  String s = "";
  while(Serial.available()){  
    s = Serial.readString();
    Serial.print(actionHandler(s));
  }
}
