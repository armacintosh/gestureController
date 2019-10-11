# Generated with SMOP  0.41
from libsmop import *
# clearBuffer.m

    
@function
def clearBuffer(myo=None,*args,**kwargs):
    varargin = clearBuffer.varargin
    nargin = clearBuffer.nargin

    if myo.tEMG.BytesAvailable > 128:
        while (myo.tEMG.BytesAvailable >= 16):

            read(myo.tEMG,16,'int8')

    
    if myo.tAccel.BytesAvailable > 20:
        while (myo.tAccel.BytesAvailable >= 20):

            read(myo.tAccel,20,'uint8')

    
    if myo.tGyro.BytesAvailable > 20:
        while (myo.tGyro.BytesAvailable >= 20):

            read(myo.tGyro,20,'uint8')

    
    if myo.tOrient.BytesAvailable > 24:
        while (myo.tOrient.BytesAvailable >= 24):

            read(myo.tOrient,24,'uint8')

    
    if myo.tEvent.BytesAvailable > 1:
        while (myo.tEvent.BytesAvailable >= 1):

            read(myo.tEvent,1,'uint8')

    
    # check
# fprintf ('tEMG BytesAvailable == #i \n',myo.tEMG.BytesAvailable);
# fprintf ('tAccel BytesAvailable == #i \n',myo.tAccel.BytesAvailable);
# fprintf ('tEvent BytesAvailable == #i \n',myo.tEvent.BytesAvailable);