function [const] = findMyoUp(EMG, const, nargin)

% no time col. here

% case for calibration
if ~exist('nargin','var') 
    
    % filter
    fn = (const.sf/2)+1; %Hz - Nyquist Frequency - 1/2 Sampling Frequency +1
    [b,a] = butter(2,(const.low_freq/fn));% Coefficients for filter - Where 2 is the order of the filter
    pLen = round(0.2*length(EMG)); % pad array
    EMGp = padarray(EMG,pLen,'symmetric','both');
    EMGfil = filtfilt(b,a,EMGp); % filter
    EMGuse = EMGfil(pLen+1:end-pLen,:); % remove the padded elements
    
else 
    
    EMGuse = EMG;
    
end


%% get the Up Direction
% should work for all ch lengths

% if length(const.EMGch) == 8    
if const.upFinder == 2
    
    % circ data for finding extensor_sensors
    OriIncrement = pi/(size(EMGuse,2)/2);
    ori = 0 : OriIncrement : 2*pi - OriIncrement; % position of each sensor around the unit circle

    % REASON FOR CHANGE
        % at the 4/5 split. when circMean uses - values, averaging over a group
        % gives you a bad mean, because values close to pi are mirrored, so if you
        % have a mean of 2 values such as + / - 2.7 (which is between ch. 3/4 and
        % 4/5) your mean would actually be 0... this is wrong.. it should be pi.
        % FIX. circMean returns only + vals...
        % you get the same problem with a 1/8 split... either just above 0 or just
        % below 2pi, should average 0, but actually will average pi...
        % Fix... select channel for each instant and take the most commonly chosne channel...
        % test = [1 1 1 0 0 0 0 1 ];
        % test_circMean = circ_mean(ori,test,2)

    circMean = zeros(size(EMGuse,1),1); % rows
    extensor_sensors = zeros(size(EMGuse,1),2); % rows;

    for R = 1:size(EMGuse,1)
        circMean(R,:) = circ_mean(ori,EMGuse(R,:),2); % mean direction for the bin in rads, can be w 95% CI

        % select the 2 closest channels for this instant
        % deal with 1/8 split, where abs distance would not be correct
        if ( circMean(R,:) > ori(end) )
            extensor_sensors(R,:) = const.EMGch([end 1]); % on the buckle so first and last channels
            % do not sort 1 8 combo...
        else 
           distance = abs((ori - circMean(R,:)));
           [~,DistInd] = sort(distance,2,'ascend');
           extensor_sensors(R,:) = DistInd(1:2); % the 2 highest extensor_sensors = ; 
        end

    end

    % choose the 2 most frequent channels 
    x = extensor_sensors(:); % 2 ch. in 1 col
    a = unique(x); % get the channle options 
    out = [a,histc(x(:),a)]; % get the count of top use
    [~,I] = sort(out(:,2), 'descend'); % sort count of top use

    const.extensor_sensors = out(I(1:2),1)'; % return chcannel of index with top 2 uses.

elseif const.upFinder == 1 
    
    % just use the highest channels.
    x = mean(EMGuse);
    
    % get the index with highest activity
    % I needs to say the ch. numbers
    [~,I0] = sort(x,'descend');  
    I = const.EMGch(I0); % I is the CH.
    
    % pick the higher of the 2 indicies next to the highest sensor...
    if I(1) == const.EMGch(1) 
        Cval = max(x(:,[2,end])); % the 2 next to I
        iC = x==Cval; % the larger of the 2
        
    elseif I(1) == const.EMGch(end)
        Cval = max(x(:,[1,end-1])); % the 2 next to I
        iC = x==Cval; % the larger of the 2
        
    else 
        Cval = max(x(:,[I0(1)+1,I0(1)-1])); % the 2 next to I
        iC = x==Cval; % the larger of the 2
        
    end 
    
    const.extensor_sensors(1) = I(1); % I already the Channel
    const.extensor_sensors(2) = const.EMGch(iC); 
end 

