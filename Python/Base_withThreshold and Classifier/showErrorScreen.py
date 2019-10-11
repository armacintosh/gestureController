# Generated with SMOP  0.41
from libsmop import *
# showErrorScreen.m

    
@function
def showErrorScreen(const=None,errorText=None,*args,**kwargs):
    varargin = showErrorScreen.varargin
    nargin = showErrorScreen.nargin

    ##
    
    # CLOSE IF OPEN ALREADY
    if logical_not(isempty(findall(0,'type','figure','name','Error Notice'))):
        close_(findall(0,'type','figure','name','Error Notice'))
    
    Err.fh = copy(figure())
# showErrorScreen.m:10
    # add Icon
    axes('Position',concat([0.85,0.0,0.2,0.2]))
    imshow('Images\DashyIcon.jpg','Border','tight')
    set(gcf,'name','Error Notice','NumberTitle','off','toolbar','none','menubar','none','units','normalized','color','k','OuterPosition',concat([0.25,0.25,0.5,0.5]))
    
    Err.tx = copy(uicontrol('style','text','units','normalized','position',concat([0,0.2,1,0.6]),'BackgroundColor','black','ForegroundColor','white','fontsize',25,'string',errorText))
# showErrorScreen.m:24
    
    ## Record
    
    # show and log
    fprintf('Connection error thrown at: %s \n',datetime())
    fileID=fopen(const.logFileMatlab,'a+')
# showErrorScreen.m:37
    fprintf(fileID,'Connection error thrown at: %s \n\n',datetime())
    fclose(fileID)