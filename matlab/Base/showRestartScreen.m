function [Rst] = showRestartScreen(const, restartText)

%%

% if isfigure('Error Notice')
% use to find the right spot to put the cal window
% get(gcf, 'Position')
% CLOSE IF OPEN ALREADY
if ~isempty(findall(0,'type','figure','name','Error Notice'))
    close(findall(0,'type','figure','name','Error Notice'));
end

Rst.fh = figure();

% add Icon
axes('Position',[.25 .3 .5 .5]);
imshow('Images\checkBattery.png','Border','tight');

set(gcf,'name','Restart Notice',...
            'NumberTitle','off',...
            'toolbar','none',...
            'menubar','none',...
            'units','normalized',...
            'color','k',...
            'OuterPosition',[0 0 1 1]); % [0 0 1 1] const.calWinSetup

Rst.tx = uicontrol('style','text',...
                             'units','normalized',...
                             'position',[0 .8 1 .15],...
                             'BackgroundColor','black',...
                             'ForegroundColor','white',...
                             'fontsize',25,...
                             'string',restartText);  % 5 sec num2str(const.calTimer+3)


% quit on button press or enter
Rst.tb = uicontrol('style','toggle',...
                             'units','normalized',...
                             'position',[0.4 0.05 0.2 0.2],...
                             'backgroundcolor','y',...
                             'fontsize',20,...
                             'string','Quit',...
                             'callback',{@readyCB});  % 5 sec num2str(const.calTimer+3)
                         
set(Rst.fh, 'KeyPressFcn', {@tb_KeyPressFcn});


%% always keeps this window on top

WinOnTop(Rst.fh); 


%% Record

% show and log
fprintf('Connection error thrown at: %s \n', datetime());
fileID = fopen(const.logFileMatlab,'a+');
fprintf(fileID,'Connection error thrown at: %s \n\n', datetime());
fclose(fileID);

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


