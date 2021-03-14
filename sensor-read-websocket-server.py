# based on
# https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect

from dotenv import load_dotenv
load_dotenv()

import os
import time
import asyncio
import websockets
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

mpu = MPU9250(
  address_ak=AK8963_ADDRESS,
  address_mpu_master=MPU9050_ADDRESS_68, # 0x68
  address_mpu_slave=None,
  bus=1,
  gfs=GFS_1000,
  afs=AFS_8G,
  mfs=AK8963_BIT_16,
  mode=AK8963_MODE_C100HZ
)

# mpu.calibrate()
# mpu.calibrateAK8963()
mpu.calibrateMPU6500()
mpu.configure() # apply settings to registers

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
      str(magData[2]))

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