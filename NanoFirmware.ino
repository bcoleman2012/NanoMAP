// TO DO: make forward() backward() functions 
/* Nano MAP firmware. 
 *  Manual control buttons on pins 4 and 5
 *  Stepper motor pulse pin on 2
 *  Stepper motor direction pin on 3
 * 
 * TO DO: 
 * Implement forward() and backward() functions (nice abstraction)
 * Create automation framework. Firmware state machine needs done. 
 * 
 * 
 * 
 * 
 * USAGE: 
 * 
 * If USB is connected and a serial connection is available, the program
 * will listen at 9600 baud for commands. The commands are: 
 * b - backward N steps
 * f - forward N steps
 * o - oscillate forward N steps, and backward N steps
 * 
 * The commands require a flag afterward, in the form of an integer. 
 * A valid command is
 * b100\n
 * (i.e. type 'b' '1' '0' '0', then press enter
 * This will take it backward 100 steps. 
 * 
 * If USB is not connected, then the pushbuttons on pin 4 and 5 control 
 * the stepper motor slide. 
 * 
 * Note that limit switches are not yet implemented. Therefore, be careful with
 * what you ask the stepper motor to do!
 */


const int stepPin = 2;
const int directionPin = 3;
const int manualForward = 4; 
const int manualBackward = 5; 



void pulse(int pin, int len){
  // PIN is a digital output pin. Len is the pulse width in ms
  digitalWrite(pin,HIGH);
  delay(len);
  digitalWrite(pin,LOW);
  return;
}





void setup() {
 
  pinMode(stepPin,OUTPUT);
  pinMode(directionPin,OUTPUT);

  pinMode(manualForward,INPUT);
  pinMode(manualBackward,INPUT);

  analogReference(EXTERNAL);
  // analogReference is necessary so that the system can run off of 
  // the attached power supply / regulator pair, even when USB 5.0V
  // is attached
  
  digitalWrite(directionPin,HIGH);
  digitalWrite(stepPin,LOW);

  Serial.begin(9600);
}


bool homeAxis(){
  }; // limit switches not implemented in hardware yet


 // static (global) ints for hacky command line interface
 int command = 0;
 int serialValue = 0;
 int speed_delay = 10; // ms
 
void loop() {
  int direction_status = 0; // 1 corresponds to high directino pin
 if( Serial.available())
 {
   Serial.print("READY\n"); 
   char ch = Serial.read();
   if (ch == 'b'){
    Serial.print("B \n");
    command = 1; // backward n steps
   }
   else if (ch == 'f'){
    Serial.print("F \n");
    command = 2; // forward n steps
   }
   else if (ch == 'o'){
    Serial.print("O \n");
    command = 3; // oscillate forward then back
   }
   else if (ch == 's'){
    Serial.print("S \n"); 
    command = 4; // speed change command
   }
   else if(ch >= '0' && ch <= '9')   {           // is ch a number?  
     serialValue = serialValue * 10 + ch - '0';           // yes, accumulate the integer value in serialValue

     Serial.print("\n");
   }
   else  // its not a digit so terminate the input    
   {
       if (command == 1){ // backward
        Serial.print("B ");
        Serial.print(serialValue);
        Serial.print(" steps\n");
        digitalWrite(directionPin,HIGH);
        for (int i = 0; i<serialValue; i++){
        // Serial.print("step\n");
        pulse(stepPin,1);
        delay(speed_delay);
      }
       }
       else if (command == 2){
         Serial.print("F ");
        Serial.print(serialValue);
        Serial.print(" steps\n");
      digitalWrite(directionPin,LOW);
        for (int i = 0; i<serialValue; i++){
      //Serial.print("step\n");
        pulse(stepPin,1);
        delay(speed_delay);
      }
       }
       else if (command == 3){
        Serial.print("Osc ");
        Serial.print(serialValue);
        Serial.print(" steps\n");
      digitalWrite(directionPin,LOW);
        for (int i = 0; i<serialValue; i++){
        // Serial.print("step\n");
        pulse(stepPin,1);
        delay(speed_delay);
      }
      digitalWrite(directionPin,HIGH);
        for (int i = 0; i<serialValue; i++){
        // Serial.print("step\n");
        pulse(stepPin,1);
        delay(speed_delay);
      }
       }
       else if (command == 4){
        Serial.print("Speed Change"); 
        Serial.print(serialValue); 
        if (serialValue >= 2)
        {
          speed_delay = serialValue; 
        }
       }

       Serial.print("OP: ");
       Serial.print(serialValue);
       Serial.print("\t");
       Serial.print(command);
       Serial.print("\n");
       serialValue = 0;
       command = 0;
       Serial.print("EXIT\n"); 
   }
 }
 else 
 {
  // if serial is not available, let's go for hardware actuation

  if (digitalRead(manualForward) == LOW)
  {
    // lets go forward
    digitalWrite(directionPin,LOW);
    pulse(stepPin,2);
    delay(8);
  }
  if (digitalRead(manualBackward) == LOW)
  {
    digitalWrite(directionPin,HIGH);
    pulse(stepPin,2);
    delay(8);
  }
 }
}

 

