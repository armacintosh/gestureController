function [out] = evalAccel (const, out, store)

% get last few second of acceleration activity, % out.normAccel = store.AccelRes(end);
out.normAccel = max(store.AccelRes(end-(const.runningAvg) : end)); % 5 seconds

% maxAccel is thresh
if (out.currentMaxAccel - out.currentBaseAccel) < std(store.AccelRes) % this is a small variance - normal for still gestures
    out.maxAccel = out.currentMaxAccel + (( (out.currentMaxAccel - out.currentBaseAccel) * 2) * const.aboveBaseAccel) ; % multiplier
else
    out.maxAccel = out.currentMaxAccel + (( (out.currentMaxAccel - out.currentBaseAccel) / 2) * const.aboveBaseAccel) ; % multiplier
end

% decide to give IMU feedback or not.
if out.normAccel > out.maxAccel    
    out.PredAccel = 1;
else
    out.PredAccel = 0;
end
