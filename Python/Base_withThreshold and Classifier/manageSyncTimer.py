# Generated with SMOP  0.41
from libsmop import *
# manageSyncTimer.m

    
@function
def manageSyncTimer(const=None,syncTimer=None,myoServerTime=None,*args,**kwargs):
    varargin = manageSyncTimer.varargin
    nargin = manageSyncTimer.nargin

    # manage the SyncTimer
    if const.calibrating == 1:
        # make syncTimer visible
#             set(syncTimer.h, 'visible','on'); #
#             const.pushbutton.AppActivate('Myo Jumper'); 
            # update 
#             myoServerTime = datestr(myo.lastTimeEMG,const.dateFormat); # time from EMG myoServer
        set(syncTimer.h2,'String',myoServerTime)
        drawnow
    
    
    # close when done
    if const.DashyOpened == 1:
        # close the syncTimer
        close_('SyncTimer')
        clear('syncTimer')
        const.useSyncTimer = copy(0)
# manageSyncTimer.m:20
    