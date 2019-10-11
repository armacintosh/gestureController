# Generated with SMOP  0.41
from libsmop import *
# validatecalData.m

    
@function
def validatecalData(const=None,out=None,store=None,state=None,calData=None,myo=None,*args,**kwargs):
    varargin = validatecalData.varargin
    nargin = validatecalData.nargin

    ## remove the first row of cal data
    
    calData.cal = copy(calData.cal(arange(2,end()),arange()))
# validatecalData.m:5
    ##  Check and Pass if NAN data errors
    
    # check that calData is valid  before processing, if not valid, reset and replay astro
    NrNaN=sum(isnan(ravel(calData.cal)))
# validatecalData.m:10
    # should have at least WINBIN * active seconds * loops/per second == rows
    if (NrNaN > 0) or state.hadError == 1:
        # run error process to retry the game
        try:
            if isempty(findobj('type','figure','name','Restart Notice')):
                const,myo,state,timestart=errorProcess(const,state,nargout=4)
# validatecalData.m:18
        finally:
            pass
        # reset statuss
        const.playAstro = copy(0)
# validatecalData.m:30
        const,state=resetKeyToggle(const,state,nargout=2)
# validatecalData.m:31
        state.hadError = copy(0)
# validatecalData.m:32
    else:
        # calculate Ready mean
        const=findReadyMean(const,calData)
# validatecalData.m:38
        # find extensor sensors
        const,out=selectEFChannels(const,out,calData,nargout=2)
# validatecalData.m:41
        # relative to cols of out.dataEMG, which includes time in col. 1
        # get the expected max F and E
        const,out,store=updateInit(const,out,calData,store,nargout=3)
# validatecalData.m:46
        if const.useClassifier == 1:
            const=setupClassifier(const)
# validatecalData.m:50
        # say dashy can start
        const.goDashy = copy(1)
# validatecalData.m:54
        const.finishedJumper = copy(1)
# validatecalData.m:55
    