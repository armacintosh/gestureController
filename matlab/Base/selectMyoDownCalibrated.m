function const = selectMyoDownCalibrated (const)

try
    % to define: from First Day Calibration, know how far flexors are
        % relative to extensors, then on new day, when you find the new
        % extensor location, put the flexors in the same relative position
        % const.flexorDistance-- only there if using a calib. profile
        % to recreate/ find the flexor sensor given the extensor sensor and the
        % flesorDistance, do: extensor_sensor - (flexorDistance);
    const.flexor_sensors = const.extensor_sensors - const.flexorDistance;

    % Adjust sensor locations depending on offset being out of ch range and

    % overlapping?
    overlap = ismember(const.extensor_sensors,const.flexor_sensors);
    if overlap (1) || overlap (2)
        disp('overlapping e f channles');

            % shuld change to: 
                % if overlap, pick sensor next to the non-overlapping
                % flexor that is not an extensor sensor
                % this happens becuase I am not sorting them...
                
                
            % just use opposite sensors
            lookaway = ( length(const.EMGch) / 2);

            if const.extensor_sensors(1) < lookaway + 1
                opposite_sensors(1) = const.extensor_sensors(1) + lookaway;
            else
                opposite_sensors(1) = const.extensor_sensors(1) - lookaway;
            end

            if const.extensor_sensors(2) < lookaway + 1
                opposite_sensors(2) = const.extensor_sensors(2) + lookaway;
            else
                opposite_sensors(2) = const.extensor_sensors(2) - lookaway;
            end

%             opposite_sensors = sort(opposite_sensors);
            const.flexor_sensors = const.EMGch(opposite_sensors);

    end 

    % out of range?
    % >8 case
    if const.flexor_sensors(1) > const.EMGch(end) % 8 
       const.flexor_sensors(1) = const.flexor_sensors(1) - length(const.EMGch);
    end

    % if only ch2 is > 8, then loop back to 1.
    if const.flexor_sensors(2) > const.EMGch(end) 
       const.flexor_sensors(2) = const.flexor_sensors(2) - length(const.EMGch);
    end

    % - case
    if const.flexor_sensors(1) < const.EMGch(1) % 8 
       const.flexor_sensors(1) = const.flexor_sensors(1) + length(const.EMGch);
    end

   if const.flexor_sensors(2) < const.EMGch(1) % if only ch2 is > 8, then loop back to 1.
      const.flexor_sensors(2) = const.flexor_sensors(2) + length(const.EMGch);
   end

%            % NEED TO CHANGE SO THAT CANNOT GET VAL > 8
%            if const.flexor_sensors(1) > const.EMGch % 8 
%                const.flexor_sensors(1) = const.flexor_sensors(1) - const.EMGch;
%            end
%            if const.flexor_sensors(2) > const.EMGch % if only ch2 is > 8, then loop back to 1.
%               const.flexor_sensors(2) = const.flexor_sensors(2) - const.EMGch;
%            end

% double check for overlapping
const = checkEFOverlap (const);

% if there is no flexor distnace, assume the opposite side    
catch 

    % else, assume flexor sensors are the opposite side.
    % must have even number of sensors..
        %     const.EMGch = 1:7; % FOR TESTING
        %     const.extensor_sensors = [4 5];

    lookaway = round ( length(const.EMGch) / 2) ;
%     % get the index as far away as possible from the extensor index.
     dist1 = abs( const.EMGch - const.extensor_sensors(1));
     FI1 = dist1==0 + lookaway;

     dist2 = abs( const.EMGch - const.extensor_sensors(2));
     FI2 = dist2==0 + lookaway;

     const.flexor_sensors(1) = const.EMGch(FI1);
     const.flexor_sensors(2) = const.EMGch(FI2);
%      const.flexor_sensors = sort(const.flexor_sensors);


end
