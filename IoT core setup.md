Raspberry Pi and Cloud IoT Core Basics Step-by-step:

Author: Gabe Weiss <gweiss@google.com>


see also:

GitHub: https://github.com/GabeWeiss/IoT_Core_Quick_Starts

Twitter: @GabeWeiss_


Note that these instructions double as a self-guide for myself in doing a live demo of this content, so some of the instructions revolve around being sure I have a clean demo environment, or customizing my personal environment to make my life easier. E.g. Changing keyboard layout on the PI obviously can be safely ignored if you’re in the UK.


Note: For this, I flash full Raspbian to my PI because the cryptography Python library requires python3 and the thin install doesn’t include Python 3, only 2. Cryptography requires Python 3, and is now used instead of pycrypto in the jwt library, which is what Cloud IoT Core uses for authentication. You can just do Raspbian Light, and then install Python 3 if that ends up being easier.


Clean laptop to be sure we’re back to zero
Edit ~/.ssh/known_hosts to remove the entry for the PI. It changes every install.
Basic device config to make it easier to use (if using monitor)
Change keyboard layout in preferences to US->English
Change font in terminal to Monospace 14
Basic device config (general)
Configure wifi
Fetch list of wifi networks available
`sudo iwlist wlan0 scan`
Configure one
`sudo vi /etc/wpa_supplicant/wpa_supplicant.conf`
Replace contents of that file with:
If there’s a password:
ctrl_interface=/var/run/wpa_supplicant

network={
   ssid=”<ssid>”
   psk=”<password for network>”
}
If there’s no password:
ctrl_interface=/var/run/wpa_supplicant

network={
   ssid=”<ssid>”
   key_mgmt=NONE
}
Restart wpa_supplicant service to engage wlan0
`sudo wpa_cli reconfigure`
Verify wlan0 is now working
`ifconfig wlan0 | grep inet` should have an IP address
If it fails, you can use `wpa_supplicant -iwlan0 -c /etc/wpa_supplicant.conf & dhcpcd wlan0` to restart it without rebooting
`sudo apt-get update`
Required modules for cryptography which pyjwt uses now instead of pycrypto
`sudo apt-get install build-essential`
`sudo apt-get install libssl-dev`
`sudo apt-get install python-dev`
`sudo apt-get install libffi-dev`
Prep the Cloud account (only need to do once)
Enable billing
Enable Cloud IoT API (done via clicking onto IoT Core pantheon)
Create a Pub/Sub Topic
Create a Pub/Sub subscription for the topic
Create an IoT Core registry
Add device to IoT Core
Create ssl certificate
`mkdir ~/.ssh`
`cd ~/.ssh`
`openssl req -x509 -newkey rsa:2048 -keyout demo_private.pem -nodes -out demo.pub -subj "/CN=unused"`
Add device to IoT Core registry created above using pantheon
Grab Google's root certificate
`wget https://pki.google.com/roots.pem`
Prep the Device
Install Sense HAT API (looks like this is already present on PI model 3)
https://www.raspberrypi.org/documentation/hardware/sense-hat/
`sudo pip3 install sense-hat`
install paho mqtt
http://www.steves-internet-guide.com/into-mqtt-python-client/
`sudo pip3 install paho-mqtt`
install json web tokens
https://pyjwt.readthedocs.io/en/latest/
`sudo pip3 install pyjwt`
install cryptography (required by encoding in PyJWT)
https://cryptography.io/en/latest/
sudo pip3 install cryptography
Write the code
See 01_basics.py
Run it
`python3 01_basics.py`
Verify data in pub/sub topic/subscription
`gcloud beta pubsub subscriptions pull --max-messages=3 <subscription id from Prep the Cloud section>`
