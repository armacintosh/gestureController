function [IMUb,EMGb] = classifyCalibrations_binDataIMU(IMU,EMGb,const)

% matches the number of bins from the EMG Bin.
Dd = IMU{:,2:end}; % removes Time

% WINBIN rows * NCH cols * N Frames of time
remainder = rem(size(Dd,1),round(const.WINBIN/4)); % scrap the last ones if it doesnt fit
x = Dd(1:end-remainder,:);
x = x';
x = x(:);

Db = permute(reshape(x, size(Dd,2), round(const.WINBIN/4), []),[2 1 3]); % splits into 20 rows, 10 cols, N bins


% Take the smaller of the 2 binned samples
nBinsEMG = size(EMGb,3);
nBinsIMU = size(Db,3);
cutTo = min([nBinsEMG,nBinsIMU]);

EMGb = EMGb(:,:,1:cutTo); 
IMUb = Db(:,:,1:cutTo);



