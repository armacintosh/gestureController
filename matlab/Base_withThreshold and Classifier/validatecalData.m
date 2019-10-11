function [const,out,store,state,calData, myo] = validatecalData (const,out,store,state,calData, myo)

%% remove the first row of cal data

calData.cal = calData.cal(2:end,:);

%%  Check and Pass if NAN data errors

% check that calData is valid  before processing, if not valid, reset and replay astro
NrNaN = sum(isnan(calData.cal(:))); 

% should have at least WINBIN * active seconds * loops/per second == rows 
if (NrNaN > 0) || state.hadError == 1 % || (NcalRows < 300)

    % run error process to retry the game
    try        
        if isempty(findobj('type','figure','name','Restart Notice')) % if window does not exist
            [const,myo,state,timestart] = errorProcess(const,state);
        end
        
    catch
        state.hadError = 1;
        const.closeTrial = 1;
        state.hadForceQuit = 1;
        state.launchedJumper = 1; % Trick game to skip playing astro.
        state.stopTrial = 1;         
    end

    % reset statuss
    const.playAstro = 0;
    [const,state] = resetKeyToggle(const,state);
    state.hadError = 0; %reset for if it happens again.
    
     
else % calibrate

    % calculate Ready mean
    const = findReadyMean (const,calData); % returns const.ReadyMean  

    % find extensor sensors
    [const, out] = selectEFChannels (const,out,calData);
    % should have const.extensor_sensors & const.flexor_sensors
    % relative to cols of out.dataEMG, which includes time in col. 1

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

