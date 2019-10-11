# Generated with SMOP  0.41
from libsmop import *
# showStretchScreen.m

    
@function
def showStretchScreen(stretchText=None,qtst=None,*args,**kwargs):
    varargin = showStretchScreen.varargin
    nargin = showStretchScreen.nargin

    Err.fh = copy(figure())
# showStretchScreen.m:4
    # add stretch image
    axes('Position',concat([0.25,0.35,0.5,0.5]))
    imshow('Images\WristStretches.gif','Border','tight')
    # add Icon
    axes('Position',concat([0.85,0.0,0.2,0.2]))
    imshow('Images\DashyIcon.jpg','Border','tight')
    set(Err.fh,'name','Stretch','NumberTitle','off','toolbar','none','menubar','none','units','normalized','Color','black','OuterPosition',concat([0,0,1,1]))
    
    # trxt
    Err.tx = copy(uicontrol('style','text','units','normalized','position',concat([0,0.85,1,0.1]),'BackgroundColor','black','ForegroundColor','white','fontsize',25))
# showStretchScreen.m:23
    
    set(Err.tx,'String',stretchText)
    
    # quit on button press or enter
    Err.tb = copy(uicontrol('style','toggle','units','normalized','position',concat([0.4,0.1,0.2,0.2]),'backgroundcolor','y','fontsize',20,'string',qtst,'callback',cellarray([readyCB])))
# showStretchScreen.m:33
    
    set(Err.fh,'KeyPressFcn',cellarray([tb_KeyPressFcn]))
    return
    
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
# showStretchScreen.m:56
    if strcmp(key,'return'):
        # close this figure
        close_(gcf)
    
    
    return
    
if __name__ == '__main__':
    pass
    