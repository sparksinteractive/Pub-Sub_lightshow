# Pub/Sub lightshow
Pub/sub lightshow runs on two separate Raspberry pis.
This repo is for the first pi which takes care of three main functions:
1. Reading knob turns, 
2. Establishing contact with Google Cloud IoT Core
    IoT core then communicates with Pub/Sub to scale up and create messages that will be held in a topic. This topic can hold upto 1 million messages per second. Which is sent back to IoT core.
3. read Config messages on IoT core to determine LED matrix animation.

### Building
Clone this repo into your raspberry pi.
In the root folder and run the following commands in terminal

```
$ pip install -r requirements.txt
$ sudo apt-get install build-essential python-dev git scons swig
$ scons
```
That should take care of all the required dependencies.

### Running
While in root folder run the main.py python script and that will start the main python script
```
$ sudo python main.py
```
### Hardware- serial communication
Once all the hardware is wired up, Make sure there is a conncetion between the Tx pin on the lightshow pi and the ticker pi. Make a connection between GND  on both Pis as well.

This should establish the physical serial connection that will show total messages or messages/sec on the ticker.

### References
Incase you run into issues, please refer to the following links.

* Neopixels on Raspberry Pi: https://learn.adafruit.com/neopixels-on-raspberry-pi/software
* Rotary encoder: https://github.com/martinohanlon/KY040
* Setting up IoT core: https://github.com/GabeWeiss/IoT_Core_Quick_Starts
* Setup config messages: https://cloud.google.com/iot/docs/how-tos/mqtt-bridge