function [param,emgF] = bayesOnlineFilter(param,Data) 
    
    % perform the filtering
    bayesSTD = zeros(size(Data));
    for j = 1:size(Data,2)
                
        for i = 1:size(Data,1)
            [bayesSTD(i,j), param.pri] = BayesFilter(Data(i,j), param.pri, param.sig, param);
         end
    end
    emgF = bayesSTD * param.sigmaMVC;


