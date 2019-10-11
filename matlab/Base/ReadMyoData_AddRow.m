   function [myo, const, state] = ReadMyoData_AddRow(myo, const,state)
    

   timestart = datetime();

   % read EMG
   bSuccess = 0;
   try
        % wait until enough data is there...
        while (myo.tEMG.BytesAvailable < 16) 
                        
            if const.errorChecking == 1
                if seconds(datetime()-timestart) > const.secondsMissing % if state.inError == 0 && const.playAstro == 1 || cosnt.DashyOpened == 1

                    const.playAstro = 0; % so that it does not collect calibration data while in error
                    fprintf('time %.2f \n', seconds(datetime()-timestart));

                    % call the Error to restart myoConnect and myoServer
                    try
                        if isempty(findobj('type','figure','name','Restart Notice')) % if window does not exist
                            [const,myo,state,timestart] = errorProcess(const,state);
                        end
                        if state.hadForceQuit == 1 || state.stopTrial == 1
                            break; % stops the while loop
                        end 
                        
                    catch
                        state.hadError = 1;
                        const.closeTrial = 1;
                        state.hadForceQuit = 1;
                        state.launchedJumper = 1; % Trick game to skip playing astro.
                        state.stopTrial = 1; 
                        
                        if state.hadForceQuit == 1
                            break; % stops the while loop
                        end 
                    end

                end
            end
            
            
        end

        % reading myo data from myoserver (one row)
        dataRead = read(myo.tEMG, 16, 'int8');  
        bSuccess = 1;
        myo.lastTimeEMG = datenum(datetime());        
    
   catch
        bSuccess = 0;
   end
   
   % if it reads data, then put it into a emgData
   if (bSuccess == 1)
       timeInput = dataRead(1:8);
       myo.emgData(myo.emgDataIndex,1) = typecast(int8(timeInput), 'uint64');
       myo.emgData(myo.emgDataIndex,2) = myo.lastTimeEMG;
       myo.emgData(myo.emgDataIndex,3:10) = dataRead(9:16);
       myo.emgDataIndex = myo.emgDataIndex + 1;
   end    
      
%    read accelerometer
   bSuccess = 0;
   try
        if (myo.tAccel.BytesAvailable >= 20)
            dataRead = read(myo.tAccel, 20, 'uint8');
            bSuccess = 1;
            myo.lastTime = datenum(datetime());
        end
   catch
    bSuccess = 0;
    if (datetime() -  myo.lastTime > 1)
        % samples dropped
    end
   end
   if (bSuccess == 1)
       timeInput = dataRead(1:8);
       myo.accelData(myo.accelDataIndex,1) = typecast(uint8(timeInput), 'uint64');
       myo.accelData(myo.accelDataIndex,2) = myo.lastTime;
       myo.accelData(myo.accelDataIndex,3) = typecast(uint8(dataRead(9:12)), 'single');
       myo.accelData(myo.accelDataIndex,4) = typecast(uint8(dataRead(13:16)), 'single');
       myo.accelData(myo.accelDataIndex,5) = typecast(uint8(dataRead(17:20)), 'single');
       myo.accelDataIndex = myo.accelDataIndex + 1;
   end

   
   
%    read gyro
   bSuccess = 0;
   try
        if (myo.tGyro.BytesAvailable >= 20)
            dataRead = read(myo.tGyro, 20, 'uint8');
            bSuccess = 1;
            myo.lastTime = datenum(datetime());
        end
   catch
    bSuccess = 0;
    if (datetime() -  myo.lastTime > 1)
        % samples dropped
    end    
   end
   if (bSuccess == 1)
       timeInput = dataRead(1:8);
       myo.gyroData(myo.gyroDataIndex,1) = typecast(uint8(timeInput), 'uint64');
       myo.gyroData(myo.gyroDataIndex,2) = myo.lastTime;
       myo.gyroData(myo.gyroDataIndex,3) = typecast(uint8(dataRead(9:12)), 'single');
       myo.gyroData(myo.gyroDataIndex,4) = typecast(uint8(dataRead(13:16)), 'single');
       myo.gyroData(myo.gyroDataIndex,5) = typecast(uint8(dataRead(17:20)), 'single');
       myo.gyroDataIndex = myo.gyroDataIndex + 1;
   end

%    read orientation
   bSuccess = 0;
   try
        if (myo.tOrient.BytesAvailable >= 24)
            dataRead = read(myo.tOrient, 24, 'uint8');
            bSuccess = 1;
            myo.lastTime = datenum(datetime());
        end
   catch
    bSuccess = 0;
    if (datetime() -  myo.lastTime > 1)
        % samples dropped
    end    
   end
   if (bSuccess == 1)
       timeInput = dataRead(1:8);
       myo.orientData(myo.orientDataIndex,1) = typecast(uint8(timeInput), 'uint64');
       myo.orientData(myo.orientDataIndex,2) = myo.lastTime;
       myo.orientData(myo.orientDataIndex,3) = typecast(uint8(dataRead(9:12)), 'single');
       myo.orientData(myo.orientDataIndex,4) = typecast(uint8(dataRead(13:16)), 'single');
       myo.orientData(myo.orientDataIndex,5) = typecast(uint8(dataRead(17:20)), 'single');
       myo.orientData(myo.orientDataIndex,6) = typecast(uint8(dataRead(21:24)), 'single');
       myo.orientDataIndex = myo.orientDataIndex + 1;
   end

   
   %%
  % read event
   bSuccess = 0;
   try
        if (myo.tEvent.BytesAvailable > 0)
            dataRead = read(myo.tEvent, 1, 'int8'); 
            bSuccess = 1;
            myo.lastTime = datenum(datetime());
        end    
   catch
    bSuccess = 0;
   end
   
   if (bSuccess == 1)
       myo.eventData(myo.eventDataIndex,1) = myo.lastTime; % so it corresponds to EMG
       myo.eventData(myo.eventDataIndex,2) = dataRead; % so it corresponds to EMG
       myo.eventDataIndex = myo.eventDataIndex + 1;
   end

   
    % EVENT CODES 
    % 1: Connected to the myo device
    % 2: No data received from the myo device since {0}, attempting reconnection...
    % 3: Connected to the MyoConnect application
    % 4: Couldn't connect to the MyoConnect application, last timestamp {0}
    % 5: first time EMG data is received   

