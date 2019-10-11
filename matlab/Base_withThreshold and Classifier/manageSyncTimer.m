function [const] = manageSyncTimer(const, syncTimer, myoServerTime)

        % manage the SyncTimer
        if const.calibrating == 1 
            % make syncTimer visible
%             set(syncTimer.h, 'visible','on'); %
%             const.pushbutton.AppActivate('Myo Jumper'); 
            % update 
%             myoServerTime = datestr(myo.lastTimeEMG,const.dateFormat); % time from EMG myoServer 
            set(syncTimer.h2, 'String', myoServerTime); %
            drawnow;
                        
        end
        
        % close when done
        if const.DashyOpened == 1 % done sync and playing
            % close the syncTimer
            close SyncTimer; % close the figure 
            clear syncTimer; % remove the variable
            const.useSyncTimer = 0;
        end
