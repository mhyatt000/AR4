import numpy as np
from pyfirmata import Arduino, util

board = Arduino("COM3")  # replace 'COM3' with your port


Step = ["J1..J9Step"]
def driveLimit(Steps, SpeedVal):

    # Assuming the global variables
    global maxSpeedDelay, minSpeedDelay
    DirPins = [_ for _ in range(9)]

    Jdone = np.zeros(9, dtype=int)
    Jcomplete = np.zeros(9, dtype=int)

    calcStepGap = (maxSpeedDelay - ((SpeedVal / 100) * maxSpeedDelay)) + minSpeedDelay + 300

    # SET CAL DIRECTION
    board.digital[J1dirPin].write(1)
    board.digital[J2dirPin].write(1)
    board.digital[J3dirPin].write(0)
    board.digital[J4dirPin].write(0)
    board.digital[J5dirPin].write(1)
    board.digital[J6dirPin].write(0)
    board.digital[J7dirPin].write(0)
    board.digital[J8dirPin].write(0)
    board.digital[J9dirPin].write(0)

    int curRead;
    
    int J1CurState;
    int J2CurState;
    int J3CurState;
    int J4CurState;
    int J5CurState;
    int J6CurState;
    int J7CurState;
    int J8CurState;
    int J9CurState;
    int DriveLimInProc = 1;

    if (J1Step <= 0 ) {
    J1complete = 1;
    }
    if (J2Step <= 0) {
    J2complete = 1;
    }
    if (J3Step <= 0) {
    J3complete = 1;
    }
    if (J4Step <= 0) {
    J4complete = 1;
    }
    if (J5Step <= 0) {
    J5complete = 1;
    }
    if (J6Step <= 0) {
    J6complete = 1;
    }
    if (J7Step <= 0) {
    J7complete = 1;
    }
    if (J8Step <= 0) {
    J8complete = 1;
    }
    if (J9Step <= 0) {
    J9complete = 1;
    }


    while (DriveLimInProc == 1) {

    //EVAL J1
    if (digitalRead(J1calPin) == LOW) {
      J1CurState = LOW;
    }
    else {
      delayMicroseconds(10);
      if (digitalRead(J1calPin) == LOW) {
        J1CurState = LOW;
      }
      else {
        delayMicroseconds(10);
        if (digitalRead(J1calPin) == LOW) {
          J1CurState = LOW;
        }
        else {
          delayMicroseconds(10);
          if (digitalRead(J1calPin) == LOW) {
            J1CurState = LOW;
          }
          else {
            J1CurState = digitalRead(J1calPin);
          }
        }
      }
    }

    //EVAL J2
    if (digitalRead(J2calPin) == LOW) {
      J2CurState = LOW;
    }
    else {
      delayMicroseconds(10);
      if (digitalRead(J2calPin) == LOW) {
        J2CurState = LOW;
      }
      else {
        delayMicroseconds(10);
        if (digitalRead(J2calPin) == LOW) {
          J2CurState = LOW;
        }
        else {
          delayMicroseconds(10);
          if (digitalRead(J2calPin) == LOW) {
            J2CurState = LOW;
          }
          else {
            J2CurState = digitalRead(J2calPin);
          }
        }
      }
    }

    //EVAL J3
    if (digitalRead(J3calPin) == LOW) {
      J3CurState = LOW;
    }
    else {
      delayMicroseconds(10);
      if (digitalRead(J3calPin) == LOW) {
        J3CurState = LOW;
      }
      else {
        delayMicroseconds(10);
        if (digitalRead(J3calPin) == LOW) {
          J3CurState = LOW;
        }
        else {
          delayMicroseconds(10);
          if (digitalRead(J3calPin) == LOW) {
            J3CurState = LOW;
          }
          else {
            J3CurState = digitalRead(J3calPin);
          }
        }
      }
    }

    //EVAL J4
    if (digitalRead(J4calPin) == LOW) {
      J4CurState = LOW;
    }
    else {
      delayMicroseconds(10);
      if (digitalRead(J4calPin) == LOW) {
        J4CurState = LOW;
      }
      else {
        delayMicroseconds(10);
        if (digitalRead(J4calPin) == LOW) {
          J4CurState = LOW;
        }
        else {
          delayMicroseconds(10);
          if (digitalRead(J4calPin) == LOW) {
            J4CurState = LOW;
          }
          else {
            J4CurState = digitalRead(J4calPin);
          }
        }
      }
    }

    //EVAL J5
    if (digitalRead(J5calPin) == LOW) {
      J5CurState = LOW;
    }
    else {
      delayMicroseconds(10);
      if (digitalRead(J5calPin) == LOW) {
        J5CurState = LOW;
      }
      else {
        delayMicroseconds(10);
        if (digitalRead(J5calPin) == LOW) {
          J5CurState = LOW;
        }
        else {
          delayMicroseconds(10);
          if (digitalRead(J5calPin) == LOW) {
            J5CurState = LOW;
          }
          else {
            J5CurState = digitalRead(J5calPin);
          }
        }
      }
    }

    //EVAL J6
    if (digitalRead(J6calPin) == LOW) {
      J6CurState = LOW;
    }
    else {
      delayMicroseconds(10);
      if (digitalRead(J6calPin) == LOW) {
        J6CurState = LOW;
      }
      else {
        delayMicroseconds(10);
        if (digitalRead(J6calPin) == LOW) {
          J6CurState = LOW;
        }
        else {
          delayMicroseconds(10);
          if (digitalRead(J6calPin) == LOW) {
            J6CurState = LOW;
          }
          else {
            J6CurState = digitalRead(J6calPin);
          }
        }
      }
    }

    //EVAL J7
    if (digitalRead(J7calPin) == LOW) {
      J7CurState = LOW;
    }
    else {
      delayMicroseconds(10);
      if (digitalRead(J7calPin) == LOW) {
        J7CurState = LOW;
      }
      else {
        delayMicroseconds(10);
        if (digitalRead(J7calPin) == LOW) {
          J7CurState = LOW;
        }
        else {
          delayMicroseconds(10);
          if (digitalRead(J7calPin) == LOW) {
            J7CurState = LOW;
          }
          else {
            J7CurState = digitalRead(J7calPin);
          }
        }
      }
    }

    //EVAL J8
    if (digitalRead(J8calPin) == LOW) {
      J8CurState = LOW;
    }
    else {
      delayMicroseconds(10);
      if (digitalRead(J8calPin) == LOW) {
        J8CurState = LOW;
      }
      else {
        delayMicroseconds(10);
        if (digitalRead(J8calPin) == LOW) {
          J8CurState = LOW;
        }
        else {
          delayMicroseconds(10);
          if (digitalRead(J8calPin) == LOW) {
            J8CurState = LOW;
          }
          else {
            J8CurState = digitalRead(J8calPin);
          }
        }
      }
    }

    //EVAL J9
    if (digitalRead(J9calPin) == LOW) {
      J9CurState = LOW;
    }
    else {
      delayMicroseconds(10);
      if (digitalRead(J9calPin) == LOW) {
        J9CurState = LOW;
      }
      else {
        delayMicroseconds(10);
        if (digitalRead(J9calPin) == LOW) {
          J9CurState = LOW;
        }
        else {
          delayMicroseconds(10);
          if (digitalRead(J9calPin) == LOW) {
            J9CurState = LOW;
          }
          else {
            J9CurState = digitalRead(J9calPin);
          }
        }
      }
    }



    if (J1done < J1Step && J1CurState == LOW) {
      digitalWrite(J1stepPin, LOW);
      delayMicroseconds(50);
      digitalWrite(J1stepPin, HIGH);
      J1done = ++J1done;
    }
    else {
      J1complete = 1;
    }
    if (J2done < J2Step && J2CurState == LOW) {
      digitalWrite(J2stepPin, LOW);
      delayMicroseconds(50);
      digitalWrite(J2stepPin, HIGH);
      J2done = ++J2done;
    }
    else {
      J2complete = 1;
    }
    if (J3done < J3Step && J3CurState == LOW) {
      digitalWrite(J3stepPin, LOW);
      delayMicroseconds(50);
      digitalWrite(J3stepPin, HIGH);
      J3done = ++J3done;
    }
    else {
      J3complete = 1;
    }
    if (J4done < J4Step && J4CurState == LOW) {
      digitalWrite(J4stepPin, LOW);
      delayMicroseconds(50);
      digitalWrite(J4stepPin, HIGH);
      J4done = ++J4done;
    }
    else {
      J4complete = 1;
    }
    if (J5done < J5Step && J5CurState == LOW) {
      digitalWrite(J5stepPin, LOW);
      delayMicroseconds(50);
      digitalWrite(J5stepPin, HIGH);
      J5done = ++J5done;
    }
    else {
      J5complete = 1;
    }
    if (J6done < J6Step && J6CurState == LOW) {
      digitalWrite(J6stepPin, LOW);
      delayMicroseconds(50);
      digitalWrite(J6stepPin, HIGH);
      J6done = ++J6done;
    }
    else {
      J6complete = 1;
    }
    if (J7done < J7Step && J7CurState == LOW) {
      digitalWrite(J7stepPin, LOW);
      delayMicroseconds(50);
      digitalWrite(J7stepPin, HIGH);
      J7done = ++J7done;
    }
    else {
      J7complete = 1;
    }
    if (J8done < J8Step && J8CurState == LOW) {
      digitalWrite(J8stepPin, LOW);
      delayMicroseconds(50);
      digitalWrite(J8stepPin, HIGH);
      J8done = ++J8done;
    }
    else {
      J8complete = 1;
    }
    if (J9done < J9Step && J9CurState == LOW) {
      digitalWrite(J9stepPin, LOW);
      delayMicroseconds(50);
      digitalWrite(J9stepPin, HIGH);
      J9done = ++J9done;
    }
    else {
      J9complete = 1;
    }
    //jump out if complete
    if (J1complete + J2complete + J3complete + J4complete + J5complete + J6complete + J7complete + J8complete + J9complete == 9) {
      DriveLimInProc = 0;
    }
    ///////////////DELAY BEFORE RESTARTING LOOP
    delayMicroseconds(calcStepGap);
    }

    }

