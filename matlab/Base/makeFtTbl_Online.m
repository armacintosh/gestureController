function FtTbl = makeFtTbl_Online (const, out)

% Input: emg data split into 20 rows, 10 cols, N = 1 bin in real time)
% Picks which features to calculate based on setupClasifier.m output
% Output: nRow (1 for real time) * FtTop Cols. 

% assumes out.EMG has been: 
%     Done abs, / 128
%     rest subtracted 

%% Bayes Filter

% some features use filtered data (these do not filter: SSC, ZC, WAMP)
if const.BayesFilter == 1  
    [param,out.dataEMG(:,2:end ) ] = bayesOnlineFilter(const.param,out.dataEMG(:,2:end ) ); % returns out.dataEMG filtered
    const.param = param;
    if sum(ismissing( out.dataEMG(:,2:end ) )) > 0
        fprintf('NAN in filtered EMG data \n\n');
    else
        fprintf('using filtered EMG \n\n');
    end 
    
end


%% for each top Feature, make the corresponding calculation

topFtVal = zeros(1,length(const.classify.Mdl.PredictorNames));
for topFt = 1:length (const.classify.Mdl.PredictorNames)

    % get the feature 
    calcOnFtName = char(const.classify.ftUse(topFt));
       
    % check if it contains circ
    if contains(calcOnFtName,'circ')
        calcOnFt = 'circ';
    else
        calcOnFt = calcOnFtName;
    end 
    
    % get the channel, actually want: 
    if length(const.EMGch) == 8
        calcOnCH = 1+ const.EMGch (const.EMGch == const.classify.ftChUse(topFt)) ;
    else
        [~,ii] = find(const.EMGch == const.classify.ftChUse(topFt)) ;
        calcOnCH = 1+ii; % because time col. is included below.
    end
       
    % do calculation on the corresponding feature and channel, always one frame
    switch calcOnFt
        
        % features calculated using multiple channels
        case 'CCI'
            topFtVal(1,topFt) = calcCCI(out.dataEMG(:,2:end),const); % nFrames*1
        
        case 'SCCI'              
            if ~exist ('smav','var')
                smav = calcSMAV(out.dataEMG(:,2:end)); % nFrames*nCH
            end
            topFtVal(1,topFt) = calcSCCI(smav, const); % nFrames*1    
            
        case 'circ'
            % need to modify calcCirc
            topFtVal(1,topFt) = calcCirc(out.dataEMG(:,2:end), const,calcOnFtName); % nFrames*nCircVars, Table

        case 'MADN'
            if ~exist ('madn','var') % so that it is only calculated 1x
                madn = calcMADN(out.dataEMG(:,2:end)); % nFrames*nCH
            end 
            topFtVal(1,topFt) = madn(:, calcOnCH-1);
            
        case 'SMAV'
            if ~exist ('smav','var')
                smav = calcSMAV(out.dataEMG(:,2:end)); % nFrames*nCH
            end
            topFtVal(1,topFt) = smav(:, calcOnCH-1);

           
        % features calculated within a single chanel
        case 'RMS'
            topFtVal(1,topFt) = calcRMS(out.dataEMG(:,calcOnCH)); % nFrames*nCH
        case 'MAV'    
            topFtVal(1,topFt) = calcMAV(out.dataEMG(:,calcOnCH)); % nFrames*nCH
        case 'WL'            
            topFtVal(1,topFt) = calcWL(out.dataEMG(:,calcOnCH)); % nFrames*nCH
        
        % uses Raw signal never filtered
        case 'VAR'   
            if const.BayesFilter == 1  
                topFtVal(1,topFt) = calcVAR(out.dataEMGraw(:,calcOnCH)); % nFrames*nCH        
            else 
                topFtVal(1,topFt) = calcVAR(out.dataEMG(:,calcOnCH)); % nFrames*nCH        
            end
        case 'SSC'        
            if const.BayesFilter == 1  
                topFtVal(1,topFt) = calcSSC(out.dataEMGraw(:,calcOnCH)); % nFrames*nCH        
            else
                topFtVal(1,topFt) = calcSSC(out.dataEMG(:,calcOnCH)); % nFrames*nCH        
            end
        case 'ZC'        
            if const.BayesFilter == 1  
                topFtVal(1,topFt) = calcZC(out.dataEMGraw(:,calcOnCH)); % nFrames*nCH        
            else
                topFtVal(1,topFt) = calcZC(out.dataEMG(:,calcOnCH)); % nFrames*nCH        
            end
        case 'WAMP'        
            if const.BayesFilter == 1  
                topFtVal(1,topFt) = calcWAMP(out.dataEMGraw(:,calcOnCH)); % nFrames*nCH        
            else 
                topFtVal(1,topFt) = calcWAMP(out.dataEMG(:,calcOnCH)); % nFrames*nCH        
            end
            
        % IMU features
        % mag Can use filtered data
        case 'A_AccMag'
            topFtVal(1,topFt) = calcIMUMag_OL(out.dataAccel(:,3:5 )); % nFrames*nCH
        case 'A_GyrMag'
            topFtVal(1,topFt) = calcIMUMag_OL(out.dataGyro(:,3:5 )); % nFrames*nCH                        

        % variance uses raw data
        case 'A_AccVar'
                topFtVal(1,topFt) = calcIMUVar_OL(out.dataAccel(:,3:5 )); % nFrames*nCH
        case 'A_GyrVar'
                topFtVal(1,topFt) = calcIMUVar_OL(out.dataGyro(:,3:5 )); % nFrames*nCH            

    end % END OF FEATURE CASE
        
end % end of features in FtTop

     
%% Normalize

% element wise
FtTbl = (topFtVal - const.classify.mu ) ./ const.classify.std ;

