function [Err] = showErrorScreen(const, errorText)

%%

% CLOSE IF OPEN ALREADY
if ~isempty(findall(0,'type','figure','name','Error Notice'))
    close(findall(0,'type','figure','name','Error Notice'));
end

Err.fh = figure();

% add Icon
axes('Position',[.85 .0 .2 .2]);
imshow('Images\DashyIcon.jpg','Border','tight');

set(gcf,'name','Error Notice',...
            'NumberTitle','off',...
            'toolbar','none',...
            'menubar','none',...
            'units','normalized',...
            'color','k',...
            'OuterPosition',[.25 .25 .5 .5]); % [0 0 1 1] const.calWinSetup

Err.tx = uicontrol('style','text',...
                             'units','normalized',...
                             'position',[0 0.2 1 0.6],...
                             'BackgroundColor','black',...
                             'ForegroundColor','white',...
                             'fontsize',25,...
                             'string',errorText);  % 5 sec num2str(const.calTimer+3)


%% Record

% show and log
fprintf('Connection error thrown at: %s \n', datetime());
fileID = fopen(const.logFileMatlab,'a+');
fprintf(fileID,'Connection error thrown at: %s \n\n', datetime());
fclose(fileID);

