function [const,out,store,state,calData] = validatecalData (const,out,store,state,calData)

% remove the first row of cal data
calData.cal = calData.cal(2:end,:);

% check the calData for missing
NrNaN = sum(isnan(calData.cal(:))); 
NrNaN2 = sum(isnan(const.ReadyMean(:)));

% should have at least WINBIN * active seconds * loops/per second == rows 
if (NrNaN > 0) || (NrNaN2 > 0) || state.hadError == 1 % || (NcalRows < 300)

    % reset and try to collect calibration again:
    % empty the data storage array
    calData.cal = out.dataEMG;

    % show error message 
    errorText = {'OUPS, CONNEXION PERDUE','...rétablir la connexion...'};
    showErrorScreen(const, errorText);

    % close jumper
    dos('taskkill /F /IM "MyoJumper.exe"');

    % reshow jumper
    [const] = showCalGame(const);

    % close error screen
    if ~isempty(findall(0,'type','figure','name','Error Notice'))
        close(findall(0,'type','figure','name','Error Notice'));
    end
    
    % reset statuss
    const.playAstro = 0;
    [const,state] = resetKeyToggle(const,state);
    rmfield(const,'ReadyMean');
    state.hadError = 0; %reset for if it happens again.
    
     
else % calibrate

    % find extensor sensors
    % should have const.extensor_sensors & const.flexor_sensors
    % relative to cols of out.dataEMG, which includes time in col. 1
    [const, out] = selectEFChannels (const,out,calData);

    % get the expected max F and E
    [const, out, store] = updateInit (const,out,calData,store);

    % setup classification
    if const.useClassifier == 1
        [const] = setupClassifier (const);
    end

    % say dashy can start 
    const.goDashy = 1;
    const.finishedJumper = 1;
    
end

