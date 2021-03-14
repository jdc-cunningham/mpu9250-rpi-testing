### About
This is a basic interface test of the MPU9250 IMU which I'm using in some projects related to SLAM.

I'm using the MPU9250 library [here](https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect) and I'm using [ChartJS](https://www.chartjs.org/docs/latest/) to plot the data. This is primarily a visual/calibration thing not really caring about accuracy just "it changed in this direction".

See video below demoing it.
[![YouTube thumbnail for video](./yt-thumb.JPG)](https://www.youtube.com/watch?v=FKAJO67X9RY)
### How to use
You will have to move some of this code over to your Pi which is connected to your MPU sensor. Install the related dependencies(note needs Python 3). Then just run the `sensor-read-websocket-server.py` file. You may want to test the values first before hand `and/or` run the sensor calibration stuff. This is just a minor tool for me so I didn't really spend much time on it.

The web page you'd have to open on your computer/device after running the python script above. It doesn't really matter which one runs first, as the browser keeps trying to connect to the socket server over and over.

### Optional CLI calibration
I don't actually consider this optional. You should run this. Sometimes depending on the board all will run fine or only one will. To run calibration as well:

`$python3 sensor-read-websocket-server.py` no calibration
`$python3 sensor-read-websocket-server.py all` calibrate (can also target mpu or mag only)
`$python3 sensor-read-websocket-server.py false 69` don't calibrate change bus addr

Sometimes the bus address can switch to 69 even when AD0 is not connected to anything.

### Check i2c bus
Using `$i2cdetect -y 1` can check if the sensor is showing up assuming you've properly wired it(follow MPU library). I didn't connect anything to `AD0` I am just using one sensor. Sometimes I've seen the bus address switch from `68` to `69`. This code is hardcoded to check for `68` may have to change that.

### Calibration steps/proper connection/stuff to check out
I had opened up an "issue" [here](https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect/issues/13) and I got some info for things to try to get better "functionality?". There are some interesting things regarding the mangetometer address not showing up(I thought it was a fluke generally never appeared). Also how to change the active address of an already instantiated mpu. Generally using `sudo`.

1) run `$sudo raspi-config` and enable `i2c`
2) check addresses that appear hopefully both 0x68 and 0x0C appear
  - 0x0C did not appear for me in the 4 sensors I "hot swap" tested. Not sure if it's worth restarting the Pi to be absolutely sure. Possible need to mess around with registers to get them to show up.