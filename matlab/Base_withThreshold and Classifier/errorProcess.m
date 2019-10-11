function [const,myo,state,timestart] = errorProcess(const,state)
            
%% indicate in error
% const.inError = 1;

% tell participant with figure window
if const.language == 1
    errorText = {'OUPS, lost connection','...finding connection again...'};
else
    errorText = {'OUPS, CONNEXION PERDUE','...rétablir la connexion...'};
end
[Err] = showErrorScreen(const,errorText);


%% RESET 
% these are the TCP/IP buffer objs
clear tEMG;
clear tAccel;
clear tGyro;
clear tOrient;
clear tEvent;

% clear MyoServer
dos('taskkill /F /IM "Myo Connect.exe"');
dos('taskkill /F /IM "MyoServer.exe"');
dos('taskkill /F /IM "MyoJumper.exe"');
% dos('taskkill /F /IM "cmd.exe"');

% reset Myo Connect and MyoServer
CheckMyoConnect(const);
myo = connectMyoServer(const);       

%% SHOULD CHECK AND OFFER FORCEQUIT if not finding it.

pause(1);    
hasData = myo.tEMG.BytesAvailable;
if hasData >0
    
    disp('reading data again');
    
    %% Show ready screen
    % must be connected to continute to this line
    % tell user we are connected again
        % clears bufffer
    % closes error window
    if isempty(findobj('type','figure','name','Connected again!')) % if it does not exist, make it
        [const,myo,state] = showReadyScreen(const,myo,Err,state);
    else 
        % show it
        figure(const.Ready.fh);
    end

    % something wrong here with how i set const.inError
    timestart = datetime();    
    
% catch % if not reading data, SHUT IT DOWN
else
    disp('still not reading data, forceQuit');
    
    % check battery / bluetooth adaptor message
    % tell participant with figure window
    if const.language == 1
        restartText = {"Connection problem, Let's restart and try again",'',"Please check the Myo battery and the Bluetooth connection"'};
    else
        restartText = {'Probleme de CONNEXION','Verifier que la betterie est bien charger'};
    end
    showRestartScreen(const,restartText);
  
    
end
        
