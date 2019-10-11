# Generated with SMOP  0.41
from libsmop import *
# showHoldScreen.m

    
@function
def showHoldScreen(holdText=None,*args,**kwargs):
    varargin = showHoldScreen.varargin
    nargin = showHoldScreen.nargin

    ##
    
    # use to find the right spot to put the cal window
# get(gcf, 'Position')
    
    Err.fh = copy(figure())
# showHoldScreen.m:9
    # imshow('Images\2_HandUp.PNG','Border','tight');
    
    # add Icon
    axes('Position',concat([0.85,0.0,0.2,0.2]))
    imshow('Images\DashyIcon.jpg','Border','tight')
    Err.fh = copy(set(gcf,'name','Shutting Down','NumberTitle','off','toolbar','none','menubar','none','units','normalized','Color','black','OuterPosition',concat([0,0,1,1])))
# showHoldScreen.m:16
    
    Err.tx = copy(uicontrol('style','text','units','normalized','position',concat([0.25,0.25,0.5,0.5]),'BackgroundColor','black','ForegroundColor','white','fontsize',34))
# showHoldScreen.m:24
    
    #                              'string',errorText);  # 5 sec num2str(const.calTimer+3)
    
    set(Err.tx,'String',holdText)
    