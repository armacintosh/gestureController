function const = checkEFOverlap (const)


% overlapping?
overlap = ismember(const.extensor_sensors,const.flexor_sensors);
if overlap (1) || overlap (2)
    disp('overlapping e f channles');

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

%         opposite_sensors = sort(opposite_sensors);
        const.flexor_sensors = const.EMGch(opposite_sensors);

end 



% % if overlap, assumme opposite side
% lookaway = round ( length(const.EMGch) / 2) ;
% 
% % get the index as far away as possible from the extensor index.
% dist1 = abs( const.EMGch - const.extensor_sensors(1));
% FI1 = dist1==0 + lookaway;
% 
% dist2 = abs( const.EMGch - const.extensor_sensors(2));
% FI2 = dist2==0 + lookaway;
% 
% const.flexor_sensors(1) = const.EMGch(FI1);
% const.flexor_sensors(2) = const.EMGch(FI2);
% 
