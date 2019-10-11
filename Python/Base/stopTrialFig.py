# Generated with SMOP  0.41
from libsmop import *
# stopTrialFig.m

    
@function
def stopTrialFig(const=None,*args,**kwargs):
    varargin = stopTrialFig.varargin
    nargin = stopTrialFig.nargin

    if const.stopTrialFigVisible == 1:
        visibility='on'
# stopTrialFig.m:4
    else:
        visibility='off'
# stopTrialFig.m:6
    
    figure
    clo.H = copy(set(gcf,'name','CloseTrial','visible',visibility,'NumberTitle','off','toolbar','none','menubar','none','units','normalized','OuterPosition',concat([0.9,0.05,0.1,0.1])))
# stopTrialFig.m:11
    clo.pb = copy(uicontrol('style','push','units','normalized','position',concat([0,0,1,1]),'fontsize',30,'backgroundcolor','r','string','Stop','val',0,'callback',cellarray([stp_call,clo])))
# stopTrialFig.m:19
    
@function
def stp_call(varargin=None,*args,**kwargs):
    varargin = stp_call.varargin
    nargin = stp_call.nargin

    # Callback for pushbutton, deletes one line from listbox.
    S=varargin[1]
# stopTrialFig.m:30
    S.Value = copy(1)
# stopTrialFig.m:31
    assignin('base','stopTrial',S.Value)
    close_