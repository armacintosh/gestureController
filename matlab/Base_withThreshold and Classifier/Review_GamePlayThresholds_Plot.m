function []= Review_GamePlayThresholds_Plot (const, t_id, trialData, peaks, out)


% turn time into double of n Seconds from start
timeinc =  milliseconds(trialData.time(2:end)-trialData.time(1:end-1));
timeinc = [0; timeinc] /  1000;
timeinc = cumsum(timeinc);
trialData.time = timeinc;


set(0,'DefaultFigureWindowStyle','docked');
figure('name',strcat(t_id,' EMG'));

% actual activity
plot(trialData.time,trialData.mavE,'b'); hold on;
plot(trialData.time,trialData.mavF,'r'); hold on;

% current max
plot(trialData.time,trialData.currentMaxE,':b'); hold on;
plot(trialData.time,trialData.currentMaxF,':r'); hold on;

% current baseline
plot(trialData.time,trialData.currentBaseE,'--b'); hold on;
plot(trialData.time,trialData.currentBaseF,'--r'); hold on;

%%

% plot maxima
plot(trialData.time(peaks.indE),trialData.mavE(peaks.indE),'b*','MarkerSize',15); hold on;
plot(trialData.time(peaks.indE),trialData.mavF(peaks.indE),'r*','MarkerSize',15); hold on;

% plot predicted thresholds 
plot(trialData.time,out.minE,'-.b*','linewidth',0.75,'MarkerSize',2); hold on;
plot(trialData.time,out.maxF,'-.r*','linewidth',0.75,'MarkerSize',2); hold on;

%% 

scrollplot('Min',0, 'windowsize',30); % add x-scroll to current axes
legend('E','F'); hold on;

%%

set(0,'DefaultFigureWindowStyle','docked');
figure('name',strcat(t_id,' GYRO'));

GyroResPeak = trialData.GyroRes(trialData.pressed==1);
timePeak = trialData.time(trialData.pressed==1);
maxGyroLine = ones(length(trialData.time),1)*out.maxGyroRes;

% PLOT
plot(trialData.time,trialData.GyroRes,'k'); hold on;
plot(timePeak,GyroResPeak,'r*','linewidth',0.75,'MarkerSize',2); hold on;
plot(trialData.time,maxGyroLine ,':r'); hold on;

scrollplot('Min',0, 'windowsize',30); % add x-scroll to current axes


%%







    