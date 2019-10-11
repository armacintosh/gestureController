function [out] = evalGyro (const, out, store)

%%
% get last few second of Gyroeration activity, % out.normGyro = store.GyroRes(end);
out.normGyro = max(store.GyroRes(end-(const.runningAvg) : end)); 
out.maxGyro = const.aboveBaseGyro; 

% decide to give IMU feedback or not.
if out.normGyro > out.maxGyro    
    out.PredGyro = 1;
else
    out.PredGyro = 0;
end
