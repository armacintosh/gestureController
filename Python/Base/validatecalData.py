# Generated with SMOP  0.41
from libsmop import *
# validatecalData.m

    
@function
def validatecalData(const=None,out=None,store=None,state=None,calData=None,*args,**kwargs):
    varargin = validatecalData.varargin
    nargin = validatecalData.nargin

    # remove the first row of cal data
    calData.cal = copy(calData.cal(arange(2,end()),arange()))
# validatecalData.m:4
    # check the calData for missing
    NrNaN=sum(isnan(ravel(calData.cal)))
# validatecalData.m:7
    NrNaN2=sum(isnan(ravel(const.ReadyMean)))
# validatecalData.m:8
    # should have at least WINBIN * active seconds * loops/per second == rows
    if (NrNaN > 0) or (NrNaN2 > 0) or state.hadError == 1:
        # reset and try to collect calibration again:
    # empty the data storage array
        calData.cal = copy(out.dataEMG)
# validatecalData.m:15
        errorText=cellarray(['OUPS, CONNEXION PERDUE','...rétablir la connexion...'])
# validatecalData.m:18
        showErrorScreen(const,errorText)
        dos('taskkill /F /IM "MyoJumper.exe"')
        const=showCalGame(const)
# validatecalData.m:25
        if logical_not(isempty(findall(0,'type','figure','name','Error Notice'))):
            close_(findall(0,'type','figure','name','Error Notice'))
        # reset statuss
        const.playAstro = copy(0)
# validatecalData.m:33
        const,state=resetKeyToggle(const,state,nargout=2)
# validatecalData.m:34
        rmfield(const,'ReadyMean')
        state.hadError = copy(0)
# validatecalData.m:36
    else:
        # find extensor sensors
    # should have const.extensor_sensors & const.flexor_sensors
    # relative to cols of out.dataEMG, which includes time in col. 1
        const,out=selectEFChannels(const,out,calData,nargout=2)
# validatecalData.m:44
        const,out,store=updateInit(const,out,calData,store,nargout=3)
# validatecalData.m:47
        if const.useClassifier == 1:
            const=setupClassifier(const)
# validatecalData.m:51
        # say dashy can start
        const.goDashy = copy(1)
# validatecalData.m:55
        const.finishedJumper = copy(1)
# validatecalData.m:56
    