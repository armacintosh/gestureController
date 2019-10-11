# Generated with SMOP  0.41
from libsmop import *
# calculateFeatures.m

    
@function
def calculateFeatures(const=None,out=None,store=None,*args,**kwargs):
    varargin = calculateFeatures.varargin
    nargin = calculateFeatures.nargin

    # get the features based on the data
    FtVals=makeFtTbl_Online(const,out)
# calculateFeatures.m:4
    # only real just in case
    FtVals=real(FtVals)
# calculateFeatures.m:7
    # predict
    predicted=predict(const.classify.Mdl,FtVals)
# calculateFeatures.m:10
    
    fprintf('\n predicted label is:  %i \n',predicted)
    # put to output
    out.FtVals = copy(FtVals)
# calculateFeatures.m:14
    out.PredLabel = copy(predicted)
# calculateFeatures.m:15
    ##
    
    # get the tendancy over the last Store series
   # takes the more popular of 1 or 2 in the store.PredLabel col
   # if they do not press 0 for a long time normGest have no values.
    HistP=store.PredLabel(arange(const.maxWindow / 2,end()))
# calculateFeatures.m:22
    
    HistP=concat([[HistP],[out.PredLabel]])
# calculateFeatures.m:23
    
    out.normGest = copy(round(median(HistP(HistP > 0))))
# calculateFeatures.m:24
    if isempty(out.normGest):
        out.normGest = copy(0)
# calculateFeatures.m:27
    
    # if nothing then make normGest == 1, 
# so that it reminds next time, to help force good movement
    if out.normGest == 1 or out.normGest == 2:
        out.normGest = copy(out.normGest)
# calculateFeatures.m:33
    else:
        out.normGest = copy(0)
# calculateFeatures.m:35
    