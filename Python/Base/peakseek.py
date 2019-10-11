# Generated with SMOP  0.41
from libsmop import *
# peakseek.m

    
@function
def peakseek(x=None,minpeakdist=None,minpeakh=None,*args,**kwargs):
    varargin = peakseek.varargin
    nargin = peakseek.nargin

    # Alternative to the findpeaks function.  This thing runs much much faster.
# It really leaves findpeaks in the dust.  It also can handle ties between
# peaks.  Findpeaks just erases both in a tie.  Shame on findpeaks.
    
    # x is a vector input (generally a timecourse)
# minpeakdist is the minimum desired distance between peaks (optional, defaults to 1)
# minpeakh is the minimum height of a peak (optional)
    
    # (c) 2010
# Peter O'Connor
# peter<dot>ed<dot>oconnor .AT. gmail<dot>com
    
    if size(x,2) == 1:
        x=x.T
# peakseek.m:15
    
    # Find all maxima and ties
    locs=find(x(arange(2,end() - 1)) >= logical_and(x(arange(1,end() - 2)),x(arange(2,end() - 1))) >= x(arange(3,end()))) + 1
# peakseek.m:18
    if nargin < 2:
        minpeakdist=1
# peakseek.m:20
    
    if nargin > 2:
        locs[x(locs) <= minpeakh]=[]
# peakseek.m:23
    
    if minpeakdist > 1:
        while 1:

            del_=diff(locs) < minpeakdist
# peakseek.m:29
            if logical_not(any(del_)):
                break
            pks=x(locs)
# peakseek.m:33
            garb,mins=min(concat([[pks(del_)],[pks(concat([false,del_]))]]),nargout=2)
# peakseek.m:35
            deln=find(del_)
# peakseek.m:37
            deln=concat([deln(mins == 1),deln(mins == 2) + 1])
# peakseek.m:39
            locs[deln]=[]
# peakseek.m:41

    
    if nargout > 1:
        pks=x(locs)
# peakseek.m:47
    
    return locs,pks
    
if __name__ == '__main__':
    pass
    