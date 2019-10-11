function [const, out] = calculateFeatures(const, out, store)

% get the features based on the data 
FtVals = makeFtTbl_Online (const, out);

% only real just in case
FtVals = real(FtVals);

% predict
predicted = predict(const.classify.Mdl,FtVals); % test 
fprintf('\n predicted label is:  %i \n', predicted);

% put to output
out.FtVals = FtVals;
out.PredLabel = predicted;

%% 

% get the tendancy over the last Store series
   % takes the more popular of 1 or 2 in the store.PredLabel col
   % if they do not press 0 for a long time normGest have no values.
HistP =  store.PredLabel(const.maxWindow/2:end); % in the last 5 seconds.
HistP = [HistP; out.PredLabel]; % adds the newest one from above
out.normGest = round(median(HistP(HistP>0)));

if isempty(out.normGest)
   out.normGest = 0;
end

% if nothing then make normGest == 1, 
% so that it reminds next time, to help force good movement       
if out.normGest == 1 || out.normGest == 2 
   out.normGest = out.normGest;
else 
   out.normGest = 0;
end

