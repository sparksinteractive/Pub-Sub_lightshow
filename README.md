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