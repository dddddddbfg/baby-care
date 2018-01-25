#include <Servo.h>
Servo myservo;
int pos=90;

int E1 = 5;
int M1 = 4;
int E2 = 6;
int M2 = 7;


byte op[40];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(M1,OUTPUT);
  pinMode(M2,OUTPUT);
  myservo.attach(9);
//  myservo.write(90);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0){

    Serial.readBytes(op,1);


    switch (op[0]){
      case 0:
        forward(10);
        Serial.println("forward");
        break;
      case 1:
        pos-=1;
        myservo.write(pos);
        delay(12);
        Serial.println("turn right");
        break;
      case 2:
        pos+=1;
        myservo.write(pos);
        delay(12);
        Serial.println("turn left");
        break;
       case 3:
         rotate(1,false);
         Serial.println("car turn right");
         break;
         
       case 4:
         rotate(1,true);
         Serial.println("car turn left");
         break;
       
       case 5:
         int degree = 0;

         //reset myservo&rotate the car
         if(pos > 90){
           degree = pos-90;   
           for(;pos>90;pos--){
              myservo.write(pos);
              delay(15);
           }
           rotate(degree,true);
         }else{
           degree = 90-pos;
           for(;pos<90;pos++){
              myservo.write(pos);
              delay(15);
           }
           rotate(degree,false);
         }
         break;
    }
  }

//  Serial.println("i am waiting");
}


int rotate(int degree, bool flag){
  int rate = 12;
  
    if(flag == true){
      digitalWrite(M1,LOW);
      digitalWrite(M2,HIGH);     
    }else{
      digitalWrite(M1,HIGH);
      digitalWrite(M2,LOW); 
    }

    Serial.println("execute");
    digitalWrite(E1,20);
    digitalWrite(E2,20);

    delay(degree*rate);
    
    digitalWrite(M1,LOW);
    digitalWrite(M2,LOW);
    digitalWrite(E1,0);
    digitalWrite(E2,0);
    
}

void forward(int distance){
    digitalWrite(M1,LOW);
    digitalWrite(M2,LOW);
    digitalWrite(E1,50);
    digitalWrite(E2,50);
    
    delay(distance*5);
    
    digitalWrite(M1,LOW);
    digitalWrite(M2,LOW);
    digitalWrite(E1,0);
    digitalWrite(E2,0);
    
}




