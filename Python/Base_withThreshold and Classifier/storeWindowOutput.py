# Generated with SMOP  0.41
from libsmop import *
# storeWindowOutput.m

    
@function
def storeWindowOutput(const=None,out=None,store=None,*args,**kwargs):
    varargin = storeWindowOutput.varargin
    nargin = storeWindowOutput.nargin

    # replace store table
    store[arange(1,end() - 1),arange()]=store(arange(2,end()),arange())
# storeWindowOutput.m:4
    
    for fieldIndex in arange(1,length(const.storeFieldNames)).reshape(-1):
        field=char(const.storeFieldNames(fieldIndex))
# storeWindowOutput.m:8
        if isfield(out,field):
            # update the last row of store with out val.
            store[end(),field]=cellarray([getattr(out,(field))])
# storeWindowOutput.m:12
    