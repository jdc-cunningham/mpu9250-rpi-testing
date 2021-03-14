#### Used libraries

* [MPU-9250 library](https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect)
* [ChartJS](https://www.chartjs.org/docs/latest/)

## About
This is a basic visual interface test of the MPU9250 IMU which I'm using in some projects related to SLAM. Primarily a visual/calibration thing not really caring about accuracy just "it changed in this direction".

See video below demoing it. <br>

[![YouTube thumbnail for video](./yt-thumb.JPG)](https://www.youtube.com/watch?v=FKAJO67X9RY)

## How to use
If you have a Raspberry PI with a GUI(not headless) you should be able to just clone this and then cd into the `pi-code` folder and install the necessary libraries(usually with `pip` note this needs Python 3).

If your Pi is headless assuming you've already gotten it connected to WiFi/have SSH access, then you just need to SFTP the python-related code to your Pi.

Then just run the `sensor-read-websocket-server.py` file. You may want to test the values first before hand `and/or` run the sensor calibration stuff. This is just a minor tool for me so I didn't really spend much time on it. Would recommend just going to the sensor library directly if you want to just view raw data in CLI.

The web page you'd have to open on your computer/device after running the python script above. It doesn't really matter which one runs first, as the browser keeps trying to connect to the socket server over and over.

## Optional CLI calibration
I don't actually consider this optional. You should run this. Sometimes depending on the board all will run fine or only one will. To run calibration as well:

`$python3 sensor-read-websocket-server.py` no calibration
`$python3 sensor-read-websocket-server.py all` calibrate (can also target mpu or mag only)
`$python3 sensor-read-websocket-server.py mpu` target only mpu, seems mag is error prone

Sometimes the bus address can switch to 69 even when AD0 is not connected to anything. The code accounts for this by testing for which bus is present on instantiation of `mpu`.

## Check i2c bus
Using `$i2cdetect -y 1` can check if the sensor is showing up assuming you've properly wired it(follow MPU library). I didn't connect anything to `AD0` I am just using one sensor. Sometimes I've seen the bus address switch from `68` to `69`.

## Calibration steps/proper connection/stuff to check out
I had opened up an "issue" [here](https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect/issues/13) and I got some info for things to try to get better "functionality?". There are some interesting things regarding the mangetometer address not showing up(I thought it was a fluke generally never appeared). Also how to change the active address of an already instantiated mpu. Generally using `sudo`.

1) run `$sudo raspi-config` and enable `i2c`
2) check addresses that appear hopefully both 0x68 and 0x0C appear
  - 0x0C did not appear for me in the 4 sensors I "hot swap" tested. Not sure if it's worth restarting the Pi to be absolutely sure. Possible need to mess around with registers to get them to show up.
