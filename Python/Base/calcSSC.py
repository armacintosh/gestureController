# Generated with SMOP  0.41
from libsmop import *
# calcSSC.m

    
@function
def calcSSC(EMGb=None,*args,**kwargs):
    varargin = calcSSC.varargin
    nargin = calcSSC.nargin

    # Number of slope sign changes of a signal
    
    # Returns the number of times the slope of the signal's
# sign changes and the absolute value of one of the slopes
# is greater than or equal to the threshold 'thresh'
    
    # signal slope change, how many times it moves over 20th percentile of the
# activity
    
    R,C,F=size(EMGb,nargout=3)
# calcSSC.m:11
    slopes=diff(EMGb,[],1)
# calcSSC.m:13
    answ=zeros(1,C,F)
# calcSSC.m:15
    for f in arange(1,F).reshape(-1):
        for i in arange(1,C).reshape(-1):
            thresh=abs(mean(prctile(slopes(arange(),i,arange()),20)))
# calcSSC.m:18
            count=0
# calcSSC.m:19
            for j in arange(1,R - 2).reshape(-1):
                if ((((slopes(j,i,f) > 0) and (slopes(j + 1,i,f) < 0)) or ((slopes(j,i,f) < 0) and (slopes(j + 1,i,f) > 0))) and ((abs(slopes(j,i,f)) >= thresh) or (abs(slopes(j + 1,i,f)) >= thresh))):
                    count=count + 1
# calcSSC.m:26
            answ[1,i,f]=count
# calcSSC.m:29
    
    answ_OUT=reshape(answ,concat([C,F])).T
# calcSSC.m:33
    ##
    
    #  OLD WAY
# [R, C] = size(binned_signal);
# slopes = diff(binned_signal,[],2);
# 
# 
# for i = 1:R # for each bin
#     count = 0;
#     for j = 1 : C-2
#         if((((slopes(i,j) > 0) && (slopes(i,j+1) < 0))...
#                 || ((slopes(i,j) < 0) && (slopes(i,j+1) > 0)))...
#                 && ((abs(slopes(i,j)) >= thresh)...
#                 || (abs(slopes(i,j+1)) >= thresh)))
#             
#         count = count + 1;
#         end
#     end
#     answ(i,:) = count;
# end
# 
# 
# end