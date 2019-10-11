# Generated with SMOP  0.41
from libsmop import *
# updateMax.m

    
@function
def updateMax(const=None,out=None,store=None,*args,**kwargs):
    varargin = updateMax.varargin
    nargin = updateMax.nargin

    # start with max and then trip based on historical max and baseline
    out.currentMaxF = copy(max(store.mavF))
# updateMax.m:4
    out.currentMaxE = copy(max(store.mavE))
# updateMax.m:5
    # updated based on last window
    
    # update the forever maxs
    if (dot(out.currentMaxE,0.75)) > const.AllTimeMaxE:
        const.AllTimeMaxE = copy(dot(out.currentMaxE,0.75))
# updateMax.m:11
    else:
        const.AllTimeMaxE = copy(const.AllTimeMaxE)
# updateMax.m:13
    
    if (dot(out.currentMaxF,0.75)) > const.AllTimeMaxF:
        const.AllTimeMaxF = copy(dot(out.currentMaxF,0.75))
# updateMax.m:17
    else:
        const.AllTimeMaxF = copy(const.AllTimeMaxF)
# updateMax.m:19
    
    
    # if have not done any flexion....(here you get really low F thresh...)
    # so have to assum E and F sensor activity are comperable.
    if out.currentMaxF < dot(out.currentBaseF,10):
        out.currentMaxF = copy(out.currentMaxE)
# updateMax.m:25
    
    
    # ensure it is not too low. 
    # too low = near threshold, near base
    if out.currentMaxE <= const.AllTimeMaxE:
        out.currentMaxE = copy(const.AllTimeMaxE)
# updateMax.m:31
    
    if out.currentMaxF <= const.AllTimeMaxF:
        out.currentMaxF = copy(const.AllTimeMaxF)
# updateMax.m:35
    