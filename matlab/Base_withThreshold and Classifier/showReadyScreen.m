function [const,myo,state] = showReadyScreen(const,myo,Err,state)


% close error window
if ~isempty(findall(0,'type','figure','name','Error Notice'))
    close(findall(0,'type','figure','name','Error Notice'));
end

% if it does not exist
if isempty(findobj('type','figure','name','Connected again!'))

%   make the connected again window
    const.Ready.fh = figure('name','Connected again!',...
                'NumberTitle','off',...
                'toolbar','none',...
                'menubar','none',...
                'units','normalized',...
                'Color','black',...
                'OuterPosition',[0 0 1 1]); % [0 0 1 1] const.calWinSetup);
           
    % add Icon
    axes('Position',[.85 .0 .2 .2]);
    imshow('Images\DashyIcon.jpg','Border','tight');

    if const.language == 1
        ReadyText = {'The connection is back !', 'Press the button "Resume game" to continue'};
        rdstr = 'Resume game';
    else
        ReadyText = {'La connexion est rétablie !', 'Appuie sur le bouton "Recommencer le jeu" pour continuer'};
        rdstr = 'Recommencer le jeu';
    end
    const.Ready.tx = uicontrol('style','text',...
                                 'units','normalized',...
                                 'position',[0 0.2 1 .8],...
                                 'BackgroundColor','black',...
                                 'ForegroundColor','white',...
                                 'fontsize',20,...
                                 'string',ReadyText);  % 5 sec num2str(const.calTimer+3)


    const.Ready.tb = uicontrol('style','toggle',...
                                 'units','normalized',...
                                 'position',[0.25 0.25 0.5 0.5],...
                                 'backgroundcolor','g',...
                                 'fontsize',20,...
                                 'string',rdstr,...
                                 'callback',{@readyCB,const,myo});  % 5 sec num2str(const.calTimer+3)

      set(gcf, 'KeyPressFcn', {@tb_KeyPressFcn,const,myo,state});

    
else 
    close(findall(0,'type','figure','name','Connected again!'));
end


end

%%
function [const, myo] = readyCB(h,event,const,myo)
    disp('in toggle callback')
        
    % clear buffer?
    clearBuffer(myo);
       
    assignin('base','inError',0);
    
    % close this figure 
    close('Connected again!');
    
    % go to Dashy and start
    if const.calibrating == 1 && ~isfield(const,'extensor_sensors')
        const.pushbutton.AppActivate('Myo Jumper'); 
    else
        const.pushbutton.AppActivate(char(const.gameLoc)); % make sure it is the same game    
    end
    
    disp('ready to change state from mouse click');
%     state.inError = 0; % reset back
        
    
end

function [const, myo,state] = tb_KeyPressFcn(h,event,const,myo,state)
    
    import java.awt.Robot;
    import java.awt.event.*;
    mouse = Robot;
    NET.addAssembly('System'); 
    import System.Diagnostics.Process.* 


    key = get(gcf,'CurrentKey');
   
    % closes on return
    if(strcmp (key , 'return'))

        disp('in toggle callback')

        % reset key
        % reset the escape key to 0
        [const,state] = resetKeyToggle(const,state);
          
        % clear buffer?
        clearBuffer(myo);

        % close this figure 
        try
            close('Connected again!');
        catch
        end
        
        % show and log it opened
        fprintf('Connection error recovered at: %s \n', datetime());
        fileID = fopen(const.logFileMatlab,'a+');
        fprintf(fileID,'Connection error recovered at: %s \n\n', datetime());
        fclose(fileID);
                    
        % go to Dashy and start
        if const.calibrating == 1 && ~isfield(const,'extensor_sensors')        
            const.pushbutton.AppActivate('Myo Jumper'); % doesnt work in full screen...
        else
            const.pushbutton.AppActivate(char(const.gameLoc)); % make sure it is the same game    
        end
        
%        assignin('base','inError',0); 
        disp('ready to change state from Enter');
%         state.inError = 0; % reset back

    end
   
end
