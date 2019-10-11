function [const, out, store] = updateBase(const,out,store)
% Update baseline

%% Extensor

% find this window's mean (SD) baseline activity (lowest seek peeks)
out.currentBaseESD = std(store.mavE);

% base
mavEinv = max(store.mavE) - store.mavE;         % invert signal.
[indEi, ~] = peakseek(mavEinv,const.minpeakdist,out.currentBaseESD); % minima
[indE, ~] = peakseek(store.mavE,const.minpeakdist,out.currentBaseESD); % maxima

% if no peaks  % ile. 
if length(indE)<5 || length(indEi)<5
    out.currentBaseE = prctile(store.mavE, 20); %
else
    out.currentBaseE = prctile (store.mavE(indEi),50);
    
    % update the forever base
    if (prctile(store.mavE(indEi),50) ) > const.AllTimeBaseE  
        const.AllTimeBaseE = prctile(store.mavE(indEi), 5); % should be the highest values 
    else 
        const.AllTimeBaseE  = const.AllTimeBaseE ;
    end 
    
    % ensure that base is not high
    if out.currentBaseE >= const.AllTimeBaseE % 
        out.currentBaseE = const.AllTimeBaseE;
    end
    
end



%% FLEXOR

% find this window's mean (SD) baseline activity (lowest seek peeks)
out.currentBaseFSD = std(store.mavF);

% base
mavFinv = max(store.mavF) - store.mavF;         % invert signal.
[indFi, ~] = peakseek(mavFinv,const.minpeakdist,out.currentBaseFSD); % minima
[indF, ~] = peakseek(store.mavF,const.minpeakdist,out.currentBaseFSD); % maxima

% if no peaks  % ile. 
if length(indF)<5 || length(indFi)<5
    
    out.currentBaseF = prctile(store.mavF, 20); %

else
    out.currentBaseF = prctile(store.mavF(indFi), 50); %
    
    % update the forever base
    if (prctile(store.mavF(indFi),50) ) > const.AllTimeBaseF 
        const.AllTimeBaseF = prctile(store.mavF(indFi), 5); % should be the highest values 
    else 
        const.AllTimeBaseF  = const.AllTimeBaseF ;
    end 
    
    % check that it is not too high 
    if out.currentBaseF >= const.AllTimeBaseF % 
        out.currentBaseF = const.AllTimeBaseF;
    end
    
end

% + fix the window change overlap...
const.lastBaseUpdate = store.time(end) + (store.time(end) -  store.time(const.jump)) ;

%% Accel

% base
AccelInv = max(store.AccelRes) - store.AccelRes;         % invert signal.
AccelSD = std(store.AccelRes);
[indAi, ~] = peakseek(AccelInv,const.minpeakdist,AccelSD); % minima
[indA, ~] = peakseek(store.AccelRes,const.minpeakdist,AccelSD); % maxima

if length(indAi)<5 || length(indA)<5
    out.currentBaseAccel = prctile(store.AccelRes, 10); % lowest all values of last 30 sec
    out.currentMaxAccel = prctile(store.AccelRes, 90); % highest all values of last 30 sec    
else
    out.currentBaseAccel = prctile(store.AccelRes(indAi), 10); % lowest base values of last 30 sec
    out.currentMaxAccel = prctile(store.AccelRes(indA), 90); % highest base values of last 30 sec
end

%% GYRO

% base
GyroInv = max(store.GyroRes) - store.GyroRes;         % invert signal.
GyroSD = std(store.GyroRes);
[indAi, ~] = peakseek(GyroInv,const.minpeakdist,GyroSD); % minima
[indA, ~] = peakseek(store.GyroRes,const.minpeakdist,GyroSD); % maxima

if length(indAi)<5 || length(indA)<5
    out.currentBaseGyro = prctile(store.GyroRes, 25); % lowest all values of last 30 sec
    out.currentMaxGyro = prctile(store.GyroRes, 95); % highest all values of last 30 sec   
else
    out.currentBaseGyro = prctile(store.GyroRes(indAi), 25); % lowest base values of last 30 sec
    out.currentMaxGyro = prctile(store.GyroRes(indA), 95); % highest base values of last 30 sec
end


