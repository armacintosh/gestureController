function [] = showStretchScreen(stretchText, qtst)


%%

% use to find the right spot to put the cal window
% get(gcf, 'Position')

Err.fh = figure();

% add stretch image
axes('Position',[.25 .35 .5 .5]);
imshow('Images\WristStretches.gif','Border','tight');

% add Icon
axes('Position',[.85 .0 .2 .2]);
imshow('Images\DashyIcon.jpg','Border','tight');

set(Err.fh,'name','Stretch',...
            'NumberTitle','off',...
            'toolbar','none',...
            'menubar','none',...
            'units','normalized',...
            'Color','black',...
            'OuterPosition',[0 0 1 1]); % [0 0 1 1] const.calWinSetup

% trxt
Err.tx = uicontrol('style','text',...
                             'units','normalized',...
                             'position',[0 0.85 1 .1],... 
                             'BackgroundColor','black',...
                             'ForegroundColor','white',...
                             'fontsize',25);%,...

set(Err.tx,'String',stretchText); % Double line!

% quit on button press or enter
Err.tb = uicontrol('style','toggle',...
                             'units','normalized',...
                             'position',[0.4 0.1 0.2 0.2],...
                             'backgroundcolor','y',...
                             'fontsize',20,...
                             'string',qtst,...
                             'callback',{@readyCB});  % 5 sec num2str(const.calTimer+3)
set(Err.fh, 'KeyPressFcn', {@tb_KeyPressFcn});

end
%%

% close when clicked
function [] = readyCB(h,event)
            
    % close this figure 
    close(gcf);
    
end

% close when pressed enter
function [] = tb_KeyPressFcn(h,event)

    key = get(gcf,'CurrentKey');
    if strcmp (key , 'return')
       
        % close this figure 
        close(gcf);
    end
   
end

