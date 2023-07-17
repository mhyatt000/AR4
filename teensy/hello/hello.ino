
int reverseSwitch = 2;  // Push button for reverse
int driverPUL = 0;    // PUL- pin
int driverDIR = 1;    // DIR- pin
int spd = A0;     // Potentiometer

// Variables

int pd = 500;       // Pulse Delay period
boolean setdir = LOW; // Set Direction
int i = 0;

// Interrupt Handler

void reverse (){ setdir = !setdir; }


void setup() {

  pinMode (driverPUL, OUTPUT);
  pinMode (driverDIR, OUTPUT);
  // if you want you can change direction with button press
  // attachInterrupt(digitalPinToInterrupt(reverseSwitch), revmotor, FALLING);
  
}


void loop() {
  
    // if you want you can toggle speed with potentiometer
    // pd = map((analogRead(spd)),0,1023,2000,50);
    digitalWrite(driverDIR,setdir);
    digitalWrite(driverPUL,HIGH);
    delayMicroseconds(pd);
    digitalWrite(driverPUL,LOW);
    delayMicroseconds(pd);
 
    if (i > 1000 || i < -1000) {
        reverse();
    }
    if (setdir) {
        i++ ;
    }
    else {
        i-- ;
    }
}
