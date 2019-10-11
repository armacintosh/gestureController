# Generated with SMOP  0.41
from libsmop import *
# showRestartScreen.m

    
@function
def showRestartScreen(const=None,restartText=None,*args,**kwargs):
    varargin = showRestartScreen.varargin
    nargin = showRestartScreen.nargin

    ##
    
    # if isfigure('Error Notice')
# use to find the right spot to put the cal window
# get(gcf, 'Position')
# CLOSE IF OPEN ALREADY
    if logical_not(isempty(findall(0,'type','figure','name','Error Notice'))):
        close_(findall(0,'type','figure','name','Error Notice'))
    
    Rst.fh = copy(figure())
# showRestartScreen.m:13
    # add Icon
    axes('Position',concat([0.25,0.3,0.5,0.5]))
    imshow('Images\checkBattery.png','Border','tight')
    set(gcf,'name','Restart Notice','NumberTitle','off','toolbar','none','menubar','none','units','normalized','color','k','OuterPosition',concat([0,0,1,1]))
    
    Rst.tx = copy(uicontrol('style','text','units','normalized','position',concat([0,0.8,1,0.15]),'BackgroundColor','black','ForegroundColor','white','fontsize',25,'string',restartText))
# showRestartScreen.m:27
    
    # quit on button press or enter
    Rst.tb = copy(uicontrol('style','toggle','units','normalized','position',concat([0.4,0.05,0.2,0.2]),'backgroundcolor','y','fontsize',20,'string','Quit','callback',cellarray([readyCB])))
# showRestartScreen.m:37
    
    
    set(Rst.fh,'KeyPressFcn',cellarray([tb_KeyPressFcn]))
    ## always keeps this window on top
    
    WinOnTop(Rst.fh)
    ## Record
    
    # show and log
    fprintf('Connection error thrown at: %s \n',datetime())
    fileID=fopen(const.logFileMatlab,'a+')
# showRestartScreen.m:57
    fprintf(fileID,'Connection error thrown at: %s \n\n',datetime())
    fclose(fileID)
    return Rst
    
if __name__ == '__main__':
    pass
    
    ##
# close when clicked
    
@function
def readyCB(h=None,event=None,*args,**kwargs):
    varargin = readyCB.varargin
    nargin = readyCB.nargin

    
    # close this figure
    close_(gcf)
    return
    
if __name__ == '__main__':
    pass
    
    # close when pressed enter
    
@function
def tb_KeyPressFcn(h=None,event=None,*args,**kwargs):
    varargin = tb_KeyPressFcn.varargin
    nargin = tb_KeyPressFcn.nargin

    key=get(gcf,'CurrentKey')
# showRestartScreen.m:79
    if strcmp(key,'return'):
        # close this figure
        close_(gcf)
    
    
    return
    
if __name__ == '__main__':
    pass
    