# Generated with SMOP  0.41
from libsmop import *
# writeWindowOutput.m

    
@function
def writeWindowOutput(const=None,out=None,*args,**kwargs):
    varargin = writeWindowOutput.varargin
    nargin = writeWindowOutput.nargin

    # writeWindowOutput to textfile
    
    # write the current out values to .txt file (only the ones designated in store).
    for fieldIndex in arange(1,length(const.storeFieldNames)).reshape(-1):
        field=char(const.storeFieldNames(fieldIndex))
# writeWindowOutput.m:7
        if isfield(out,field):
            # if it is the end dont put comma
            if fieldIndex == length(const.storeFieldNames):
                val=getattr(out,(field))
# writeWindowOutput.m:13
                fprintf(const.fileID_STORE,'%f ',val)
            else:
                if strcmp(field,'time'):
                    val=datestr(out.time,const.dateFormat)
# writeWindowOutput.m:18
                    fprintf(const.fileID_STORE,'%s,',val)
                else:
                    val=getattr(out,(field))
# writeWindowOutput.m:23
                    fprintf(const.fileID_STORE,'%f,',val)
    
    
    # add new line when done row
    fprintf(const.fileID_STORE,' \n')