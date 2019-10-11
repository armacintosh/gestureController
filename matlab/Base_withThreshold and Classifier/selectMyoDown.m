function [const] = selectMyoDown (const)


if length(const.EMGch) == 8

    if const.useUserProfile == 1
        const = selectMyoDownCalibrated (const);
    else 
        %% The way below just gets the opposite side, 
            % If I just always use opposite side, then It would work regardless of the way you put it on…
            % AND I WOULD NOT NEED TO calibrateUserProfile…
            % BUT, it would not get cases when flexors are closer to extensors… and may allow side movement…
            % if overlap, assumme opposite side

        % distance to opposite sensor
        lookaway = round ( length(const.EMGch) / 2) ;

        % get the index as far away as possible from the extensor index.
        dist1 = abs( const.EMGch - const.extensor_sensors(1));
        FI1 = dist1==0 + lookaway;

        dist2 = abs( const.EMGch - const.extensor_sensors(2));
        FI2 = dist2==0 + lookaway;

        const.flexor_sensors(1) = const.EMGch(FI1);
        const.flexor_sensors(2) = const.EMGch(FI2);
        
    end
   
else
    
     lookaway = round ( length(const.EMGch) / 2) ;

     % get the index as far away as possible from the extensor index.
     dist1 = abs( const.EMGch - const.extensor_sensors(1));
     FI1 = dist1==0 + lookaway;

     dist2 = abs( const.EMGch - const.extensor_sensors(2));
     FI2 = dist2==0 + lookaway;
     
     const.flexor_sensors(1) = const.EMGch(FI1);
     const.flexor_sensors(2) = const.EMGch(FI2);
     
end




