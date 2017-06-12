mport numpy as np
import math

ACCX_CALIB = 0.0
ACCY_CALIB = 0.0
ACCZ_CALIB = 0.0
NUM = 0.0

#finds the constance
def avg( accel )

  ACCX_CALIB = ACCX_CALIB + accel[0]
  ACCX_CALIB = ACCY_CALIB + accel[0]
  ACCX_CALIB = ACCZ_CALIB + accel[0]
  NUM = NUM + 1.0
  
  CALIB = [ ACCX_CALIB / NUM , ACCY_CALIB / NUM , ACCZ_CALIB / NUM ]
  
  return CALIB
