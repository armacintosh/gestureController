function [const, out, store] = updateInit (const,out,calData,store)

% index of when cal game went from ready to active
strtind = const.CalGoTime ;

%% 

% get the data
if const.upFinder == 1
    % used to be myo.emgCols
    senE = const.extensor_sensors(1); % sensor + time col
    senF = const.flexor_sensors(1);
elseif const.upFinder == 2
    senE = const.extensor_sensors;
    senF = const.flexor_sensors;
end 

% pre-process, remove time col.
ExRawE = calData.cal(:,senE);
ExRawF = calData.cal(:,senF);
out1 = store;

%% the 90th % value to find max start

% max is 95%ile during up phase , (after strtind)
% select the top __ percent of the trail data..
[BE,~] = sortrows(ExRawE(strtind:end,1)); % index the rows and sort by total amplitude
out.currentMaxE = prctile(BE(:,1),95); % the rows of index to keep
out1.currentMaxE(:) = out.currentMaxE; % all ros of out 1 .

[BF,~] = sortrows(ExRawF(strtind:end,1)); % index the rows and sort by total amplitude
out.currentMaxF = ( prctile(BF(:,1),100) ); 
const.MaxFlxExpected = out.currentMaxF;
out1.currentMaxF(:) = out.currentMaxF; % all ros of out 1 .


%% get Beseline

% base based on data before strtind, find SD within 10-90 %     
% only using the main channel in this case
[BERest,~] = sortrows(ExRawE(1:strtind,1)); % index the rows and sort by total amplitude
[BFRest,~] = sortrows(ExRawF(1:strtind,1)); % index the rows and sort by total amplitude

% set baseline to be mean of baseline during pre phase...
out.currentBaseE = prctile(BERest(:,:),70);
out.currentBaseF = prctile(BFRest(:,:),70);

% into 100
out1.currentBaseE(:) = out.currentBaseE;
out1.currentBaseF(:) = out.currentBaseF;


%% make a random array for mav and baseSD

% out.currentBaseFSD is 100 random from 1 SD within BFRest
RindE = randi(length(BERest),size(out1,1),1);
out1.mavE(:) = BERest(RindE);
out1.currentBaseESD(:) = std(out1.mavE);

RindF = randi(length(BFRest),size(out1,1),1);
out1.mavF(:) = BFRest(RindF);
out1.currentBaseFSD(:) = std(out1.mavF);

% rest thresholds to the base 
out1.minE = (out1.currentMaxE - out1.currentBaseESD) * const.aboveBaseE; % - const.LeewayE; 
out1.maxF = (out1.currentMaxF + out1.currentBaseFSD) * const.aboveBaseF; 


%%
% fill max of Accel.
AccelFill = prctile(store.AccelRes,90); % half store length
AccelFillarray = AccelFill* ones(size(out1,1),1);
out1.currentMaxAccel = AccelFillarray;
out1.AllTimeMaxAccel = AccelFillarray * 0.75;

store = out1;
