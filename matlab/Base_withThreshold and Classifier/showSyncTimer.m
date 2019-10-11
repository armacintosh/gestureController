function [syncTimer] = showSyncTimer()

% to sync the button press in DataLite with the EMG, the running timer has
% to be visible at the same time you manually press start in DataLite

% to updatein main 
% timeplayed = round(minutes(datetime() - handles.startTime ));
% set(handles.h2, 'String', strcat(num2str(timeplayed),' min'));

%%  Setup figure

set(0,'DefaultFigureWindowStyle','default');

handles.h = figure;        
set(gcf,'color','red','NumberTitle','off','name','SyncTimer',...
            'visible','off',...
            'toolbar','none',...
            'menubar','none',...
            'units','normalized',...
            'OuterPosition',[0 0.1 0.2 0.12]); % to change to go to just above/ below MyoJumper

handles.h1 = uicontrol('Style', 'text', 'String', '1',...
    'Units','Normalized',... 
    'Position', [0 0 1 1],'BackgroundColor','black');

handles.h2 = uicontrol('Style', 'text', 'String', '2',...
    'Units','Normalized',... 
    'Position', [0 0 1 1],'BackgroundColor','k','ForeGroundColor','w',...
    'FontSize',35);%,...

%     handles.startTime = datetime();
%     % put val in 
%     timeplayed = round(minutes(datetime() - handles.startTime ));
     set(handles.h2, 'String', strcat('00:00',':00:000')); %
%     drawnow;

syncTimer = handles;