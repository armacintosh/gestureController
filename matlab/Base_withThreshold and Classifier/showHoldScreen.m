function [] = showHoldScreen(holdText)



Err.fh = figure();

% add Icon
axes('Position',[.85 .0 .2 .2]);
imshow('Images\DashyIcon.jpg','Border','tight');

Err.fh = set(gcf,'name','Shutting Down',...
            'NumberTitle','off',...
            'toolbar','none',...
            'menubar','none',...
            'units','normalized',...
            'Color','black',...
            'OuterPosition',[0 0 1 1]); % [0 0 1 1] const.calWinSetup[.25 .25 .5 .5]

Err.tx = uicontrol('style','text',...
                             'units','normalized',...
                             'position',[.25 .25 .5 .5],...
                             'BackgroundColor','black',...
                             'ForegroundColor','white',...
                             'fontsize',34);%,...
%                              'string',errorText);  % 5 sec num2str(const.calTimer+3)


set(Err.tx,'String',holdText); % Double line!

