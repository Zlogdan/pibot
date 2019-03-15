String data,input;
boolean flag=false;
int led = 13;

int redPin = 11;
int greenPin = 10;
int bluePin = 9;
 
void setColor(int red, int green, int blue)
{
  #ifdef COMMON_ANODE
    red = 255 - red; 
    green = 255 - green;
    blue = 255 - blue;
  #endif
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue);  
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);  
  pinMode(led, OUTPUT);  
}

void loop() {
  data = Serial.readString();
  
  if (data == "led"){
    
    if(data == "on"){
      digitalWrite(led, HIGH);
      Serial.print("1\n");
    } else if(data == "off"){
      digitalWrite(led, LOW);
      Serial.print("0\n");
    } else if(data == "off"){
      digitalWrite(led, LOW);
      Serial.print("0\n");
    }else {
      Serial.print(data);
    }
  }else if(data == "rgb"){
    int i=0;
    int inChar;
    
    while(inChar != '\n') {
      
      inChar = Serial.read();
       
      if(inChar == ' ' || inChar == '\n'){
        
        rgb[i]=inString.toInt();
        Serial.print("Value:");
        Serial.println(inString.toInt());
        inString = "";
        i++;
        //inChar = Serial.read();
        continue;
      }  
    
      if (isDigit(inChar)) {
        inString += (char)inChar;
      }
      
      //inChar = Serial.read();
    }
     Serial.print(String(String(rgb[0]) + ":" + rgb[1] + ":" + rgb[2] + "\n"));
     setColor(rgb[0],rgb[1],rgb[2]);
     inString = "";
  }

  // delay(1);
}

/*
  digitalWrite(led, HIGH);
 digitalWrite(led, LOW);
 */


