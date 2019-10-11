function [EMGb,TLb] = classifyCalibrations_binDataEMG(D,const)

Dd = D{:,2:end}; % removes Time

% WINBIN rows * NCH cols * N Frames of time
remainder = rem(size(Dd,1),const.WINBIN); % scrap the last ones if it doesnt fit
x = Dd(1:end-remainder,:);
x = x';
x = x(:);

% check this
Db = permute(reshape(x, size(Dd,2), const.WINBIN, []),[2 1 3]); % splits into 20 rows, 10 cols, N bins

EMGb = Db(:,1:end-1,:); % the binned EMG data
TLb = Db(:,end,:); % the binned True Label