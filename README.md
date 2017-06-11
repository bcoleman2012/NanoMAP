## NanoMAP

### Nanoparticle Magnetic Actuation Platform

The NanoMAP is a precision actuator for superparamagnetic nanoparticles, useful for a 
variety of biomedical applications. The NanoMAP controls the movement of magnetic particles 
through microfluidic chips, allowing for the automation of ELISA, LAMP, and other assays. The NanoMAP was developed to support research projects at Asghar Lab at Florida Atlantic University. 

More information about our bioengineering lab is available [here](http://faculty.eng.fau.edu/asghar/).

#### Features
* Manual and automated actuation 
* Client-side scripting engine
* Command-based interface

### Arduino Firmware

Regardless of the hardware configuration (due to the existence of multiple and customized NanoMAP devices), to conform to the NanoMAP specification, the Arduino firmware must support a set of core commands through a serial interface. 

``` 
- b(N) // forward movement by 0.5*N millimeters (mm)
- f(N) // backward movement by 0.5*N mm
- o(N) // oscillate forward, then backward by 0.5*N mm
```

To make the platform move forward by 5 mm, for instance, send the ASCII command 
``` bash
b10
```

Support for speed control commands is planned in the future. A subset of GCODE commands may also be implemented. 

### Python Scripting Engine

A Python scripting engine is provided for rapid assay and microfluidic chip prototyping. 

#### Installation 

NanoMAP for Python depends on Pyserial. If Pyserial is not installed, 

``` bash
$ pip install pyserial
```

The NanoMAP session manager should automatically detect and connect to any authentic 
Arduino device with the right firmware. If you run the session in verbose mode but do 
not make a successful connection: 
* Make sure the device is plugged all the way in. The Arduino LED should be ON
* Close all other serial terminals with the Arduino
* Ensure that the firmware is up to date

