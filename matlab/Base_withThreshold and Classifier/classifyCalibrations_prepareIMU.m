function [const,IMU, D_IMUF] = classifyCalibrations_prepareIMU(Data, const, ind)

%%

%% Get resting data (ReadyMean)

RestUse = [ind.IMU.startTime1_rest:ind.IMU.startTime1_active,...
           ind.IMU.startTime2_rest:ind.IMU.startTime2_active,...
           ind.IMU.startTime3_rest:ind.IMU.startTime3_active...
           ];
IMUReady = Data.IMU(RestUse,:); % Get the raw resting data
ReadyMeanIMU = classifyCalibrations_findReadyMean (IMUReady); % changes const.ReadyMean;

%% FIND CORRECT IMU DATA

% Fingers Open
E2 = Data.IMU(ind.IMU.startTime1_active:ind.IMU.startTime1_end, : );
TL = ones(size(E2,1),1)*2;
E2 = [E2, array2table(TL)];

% Fingers closed
E1 = Data.IMU(ind.IMU.startTime2_active:ind.IMU.startTime2_end,: ); % E1 and startTime2 do not match on purposes (Gesture 2 is dones first in cal game)
TL = ones(size(E1,1),1);
E1 = [E1, array2table(TL)];

% Pinch
E3 = Data.IMU(ind.IMU.startTime3_active:ind.IMU.startTime3_end,: ); % E1 and startTime2 do not match on purposes (Gesture 2 is dones first in cal game)
TL = ones(size(E3,1),1)*3;
E3 = [E3, array2table(TL)];

IMU = [E2;E1;E3]; % put all gestures with TLs into single table
IMU.Properties.VariableNames = {'time' 'Accel_x' 'Accel_y' 'Accel_z' 'Gyro_x' 'Gyro_y' 'Gyro_z' 'Orient_x' 'Orient_y' 'Orient_z' 'Orient_w' 'TL'};
IMU{:,2:end-1} = IMU{:,2:end-1} - ReadyMeanIMU; % subtract resting values from all channels 

D_IMUF = IMU;
 
