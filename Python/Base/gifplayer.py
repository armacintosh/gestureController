# Generated with SMOP  0.41
from libsmop import *
# gifplayer.m

    
@function
def gifplayer(gif_image=None,delay_length=None,*args,**kwargs):
    varargin = gifplayer.varargin
    nargin = gifplayer.nargin

    # The function displays any animated GIF's in a figure window
    
    ## Demo : gifplayer; #plays the animated crystal.gif file
    
    ## Usage:
# ex: gifplayer('animated.gif',0.1); #name of the gif file and the delay in
# which to update the frames in the GIF file
    
    ## Vihang Patil, Oct 2006
# Copyright 2006-2007 Vihang Patil
# Email: vihang_patil@yahoo.com
# Created: 17th Oct 2006
    
    ## Revision:
# Date: 19th Oct 2006..Removed the setappdata and getappdata and used
# functions handling property. Multiple Gif's can be called upon which can
# be opened in new figure window.
# ex: figure;gifplayer;
# ex: figure;gifplayer('abcd.gif',0.1); and so on
# 
## P.N: PLease make sure to close the existing window in which the gif is
# currently being played and open a separate window for another GIF
# image.If another GIF is opened in the same window then the first timer
# continues to run even if you close the figure window.
    
    if nargin < 1:
        gif_image='crystal.gif'
# gifplayer.m:29
        delay_length=0.2
# gifplayer.m:30
    else:
        if nargin < 2:
            delay_length=0.2
# gifplayer.m:32
    
    pathstr,name,ext=fileparts(gif_image,nargout=3)
# gifplayer.m:35
    
    if strcmp(ext,'.gif'):
        handles.im,handles.map=imread(gif_image,'frames','all',nargout=2)
# gifplayer.m:38
        handles.len = copy(size(handles.im,4))
# gifplayer.m:39
        handles.h1 = copy(imshow(handles.im(arange(),arange(),arange(),1),handles.map,'Border','tight'))
# gifplayer.m:40
        handles.guifig = copy(gcf)
# gifplayer.m:41
        handles.guifig.Name = copy('Loading MyoDashy')
# gifplayer.m:44
        handles.guifig.NumberTitle = copy('off')
# gifplayer.m:45
        handles.guifig.MenuBar = copy('none')
# gifplayer.m:46
        handles.guifig.ToolBar = copy('none')
# gifplayer.m:47
        handles.guifig.Units = copy('normalized')
# gifplayer.m:48
        handles.guifig.OuterPosition = copy(concat([0.3,0.27,0.38,0.53]))
# gifplayer.m:49
        handles.count = copy(1)
# gifplayer.m:53
        handles.tmr = copy(timer('TimerFcn',cellarray([TmrFcn,handles.guifig]),'BusyMode','Queue','ExecutionMode','FixedRate','Period',delay_length))
# gifplayer.m:54
        guidata(handles.guifig,handles)
        start(handles.tmr)
    else:
        error('Not a GIF image. Load only GIF images')
    
    set(gcf,'CloseRequestFcn',cellarray([CloseFigure,handles]))
    
@function
def TmrFcn(src=None,event=None,handles=None,*args,**kwargs):
    varargin = TmrFcn.varargin
    nargin = TmrFcn.nargin

    #Timer Function to animate the GIF
    
    handles=guidata(handles)
# gifplayer.m:67
    set(handles.h1,'CData',handles.im(arange(),arange(),arange(),handles.count))
    
    handles.count = copy(handles.count + 1)
# gifplayer.m:69
    
    if handles.count > handles.len:
        handles.count = copy(1)
# gifplayer.m:71
    
    guidata(handles.guifig,handles)
    
@function
def CloseFigure(src=None,event=None,handles=None,*args,**kwargs):
    varargin = CloseFigure.varargin
    nargin = CloseFigure.nargin

    # Function CloseFigure(varargin)
    stop(handles.tmr)
    delete(handles.tmr)
    
    closereq