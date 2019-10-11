function [const] = setupClassifier (const)

%% Select the features to calculate (only the tops)

predictors = const.classify.Mdl.PredictorNames;
C = cellfun(@(S) strsplit(S,'_'),predictors,'Uniform', 0);
fprintf('Full Model Features: %s \n', C{1}{2} );

for topFt = 1:length(C)
    ftUse(topFt) = C{1,topFt}(2);
end

const.classify.ftUse = ftUse;


%% re-align the channels 

% % for testing
%     y = 2; % will have to do this after I have selected channels.
% %     chABS = randi([1 8], [1 7])
%     dist = chABS - y
    % is the index of the e channel... on 3/6 this means e == 4 is ch 6
    eInd = const.extensor_sensors(1) - 1 ; % const.extensor_sensors(1) is col. index of data col. 
    e = const.EMGch(eInd);
    
    dist = const.classify.FtChDist; 
%     e = 8; % new y new Extensor Channel
    % dist can be from -7 to 7, (eCH - ch1:8)
    
    ftChRaw = e + dist;
    
%     if length (const.EMGch) < 8
%         %  Get new channel for each feature
%         for ftNum = 1:length(ftChRaw)
%             % check if the distance exceeds the channels used
%             if ftChRaw(ftNum) > const.EMGch(end) 
%                 ftCh(ftNum) = ftChRaw(ftNum)  - const.EMGch(end);
%             elseif ftChRaw(ftNum) < const.EMGch(1)
%                 ftCh(ftNum) = ftChRaw(ftNum)  + const.EMGch(end);
%             else 
%                 ftCh(ftNum) = ftChRaw(ftNum);
%             end 
%            ftCh(ftNum)
%         end
%     end
    
%  Get new channel for each feature
    for ftNum = 1:length(ftChRaw)
        % check if the distance exceeds the channels used
        if ftChRaw(ftNum) > const.EMGch(end) 
            ftCh(ftNum) = ftChRaw(ftNum)  - length(const.EMGch); % length(const.EMGch)
        elseif ftChRaw(ftNum) < const.EMGch(1)
            ftCh(ftNum) = ftChRaw(ftNum)  + length(const.EMGch);
        else 
            ftCh(ftNum) = ftChRaw(ftNum);
        end 
       ftCh(ftNum)
    end
    
    %     ftCh
    % if a mulit-ch feature, then ftCh == NaN
    const.classify.ftChUse = ftCh; % col or ch.? COL
    

