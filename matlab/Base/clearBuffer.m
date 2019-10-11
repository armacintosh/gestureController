function [myo] = clearBuffer (myo)

if myo.tEMG.BytesAvailable > 128    
    while (myo.tEMG.BytesAvailable >= 16) % clear the buffer by reading all the data
        read(myo.tEMG, 16, 'int8'); % EMG data
    end
end

if myo.tAccel.BytesAvailable > 20    
    while (myo.tAccel.BytesAvailable >= 20) % clear the buffer by reading all the data
        read(myo.tAccel, 20, 'uint8');
    end
end
if myo.tGyro.BytesAvailable > 20    
    while (myo.tGyro.BytesAvailable >= 20) % clear the buffer by reading all the data
        read(myo.tGyro, 20, 'uint8');       
    end
end        
if myo.tOrient.BytesAvailable > 24    
    while (myo.tOrient.BytesAvailable >= 24) % clear the buffer by reading all the data
        read(myo.tOrient, 24, 'uint8');           
    end
end
if myo.tEvent.BytesAvailable > 1    
    while (myo.tEvent.BytesAvailable >= 1) % clear the buffer by reading all the data
        read(myo.tEvent, 1, 'uint8');           
    end
end

% check
% fprintf ('tEMG BytesAvailable == %i \n',myo.tEMG.BytesAvailable);
% fprintf ('tAccel BytesAvailable == %i \n',myo.tAccel.BytesAvailable);
% fprintf ('tEvent BytesAvailable == %i \n',myo.tEvent.BytesAvailable);