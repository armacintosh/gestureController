# Generated with SMOP  0.41
from libsmop import *
# showSyncTimer.m

    
@function
def showSyncTimer(*args,**kwargs):
    varargin = showSyncTimer.varargin
    nargin = showSyncTimer.nargin

    # to sync the button press in DataLite with the EMG, the running timer has
# to be visible at the same time you manually press start in DataLite
    
    # to updatein main 
# timeplayed = round(minutes(datetime() - handles.startTime ));
# set(handles.h2, 'String', strcat(num2str(timeplayed),' min'));
    
    ##  Setup figure
    
    set(0,'DefaultFigureWindowStyle','default')
    handles.h = copy(figure)
# showSyncTimer.m:14
    set(gcf,'color','red','NumberTitle','off','name','SyncTimer','visible','off','toolbar','none','menubar','none','units','normalized','OuterPosition',concat([0,0.1,0.2,0.12]))
    
    handles.h1 = copy(uicontrol('Style','text','String','1','Units','Normalized','Position',concat([0,0,1,1]),'BackgroundColor','black'))
# showSyncTimer.m:22
    handles.h2 = copy(uicontrol('Style','text','String','2','Units','Normalized','Position',concat([0,0,1,1]),'BackgroundColor','k','ForeGroundColor','w','FontSize',35))
# showSyncTimer.m:26
    
    #     handles.startTime = datetime();
#     # put val in 
#     timeplayed = round(minutes(datetime() - handles.startTime ));
    set(handles.h2,'String',strcat('00:00',':00:000'))
    
    #     drawnow;
    
    syncTimer=copy(handles)
# showSyncTimer.m:37