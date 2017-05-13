# Reach Data Processing

This is the repository for the data analysis side of project Reach

The main file will be a python script designed to import, process, and then export telemetry data to an external server.


### Prerequisites

Python version: developed with 2.7, may run fine with 3.x

Python libraries used:

```
pySerial

```

Arduino:
paste url: into preferences tab of the arduino ide.
from the board manager, install both the arduino SAMD boards and the adafruit SAMD boards.


## Getting Started
curenrly main file is still under construction, so files must be called individually.
in the command prompt run "python [fileYouWantToRun]"

note: for the serial port code, the serial port can only be occupied by a single process at a time, therefore upload code to the feather first, then run pyserial code.
