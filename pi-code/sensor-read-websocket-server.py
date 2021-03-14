# based on
# https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect

from dotenv import load_dotenv
load_dotenv()

import os, sys
import time
import asyncio
import websockets
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

# these are primarily for calibrating and adapting to the sensor board if it has problems
# the args method is not great, it's positional based can't be empty eg. use false for empty
# ex. $python3 sensor-read-websocket-server.py
# ex. $python3 sensor-read-websocket-server.py all
# ex. $python3 sensor-read-websocket-server.py false false true
def get_cli_args(name='default', calibrate='', address='', reset=''):
  
  global mpu

  mpu = MPU9250(
    address_ak=AK8963_ADDRESS,
    address_mpu_master=MPU9050_ADDRESS_69 if address == '69' else MPU9050_ADDRESS_68,
    address_mpu_slave=None,
    bus=1,
    gfs=GFS_1000,
    afs=AFS_8G,
    mfs=AK8963_BIT_16,
    mode=AK8963_MODE_C100HZ
  )

  mpu.configure() # apply settings to registers

  if (reset == 'man'): # ha
    print('calibrate: (all, mpu, mag), address: (68, 69), reset: (true, false)')
    print('ex: $python3 sensor-read-websocket-server.py mpu 69')

  if (reset == 'true'):
    mpu.reset()
    print('mpu reset, restart pi')
    exit()

  if (calibrate == 'all'):
    print('calibrating...')
    print('if it fails, try mpu instead of all')
    mpu.calibrateMPU6500()
    mpu.calibrateAK8963()
    mpu.configureMPU6500(mpu.gfs, mpu.afs)
    mpu.configureAK8963(mpu.mfs, mpu.mode)
  elif (calibrate == 'mpu'):
    print('calibrating...')
    mpu.calibrateMPU6500()
    mpu.configureMPU6500(mpu.gfs, mpu.afs)
  elif (calibrate == 'mag'):
    print('calibrating...')
    mpu.calibrateAK8963()
    mpu.configureAK8963(mpu.mfs, mpu.mode)

# check for cli args related to calibration
get_cli_args(*sys.argv)

async def streamMpuData(websocket, path):
  while True:
    accelData = mpu.readAccelerometerMaster()
    gyroData = mpu.readGyroscopeMaster()
    magData = mpu.readMagnetometerMaster()
    # tmpData = mpu.readTemperatureMaster() # garbage

    # this is super ugly
    dataStr = (
      str(accelData[0]) + "," +
      str(accelData[1]) + "," +
      str(accelData[2]) + "," +
      str(gyroData[0]) + "," +
      str(gyroData[1]) + "," +
      str(gyroData[2]) + "," +
      str(magData[0]) + "," +
      str(magData[1]) + "," +
      str(magData[2])
    )

    await websocket.send(
      dataStr
    )

    time.sleep(0.1)

# websocket server
# https://websockets.readthedocs.io/en/stable/intro.html (browser-based example)
# PI_ADDR if internal would be a 192... type address
start_server = websockets.serve(streamMpuData, os.getenv("PI_ADDR"), os.getenv("PI_SOCKET_PORT"))

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()