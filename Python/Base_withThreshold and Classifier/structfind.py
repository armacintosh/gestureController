# Generated with SMOP  0.41
from libsmop import *
# structfind.m

    
@function
def structfind(a=None,field=None,value=None,*args,**kwargs):
    varargin = structfind.varargin
    nargin = structfind.nargin

    # StructFind, Find the index of a certain string or value in a struct
    
    #       index=structfind(a,field,value)
    
    #  inputs,
#       a : A Matlab struct, for example a(1).name='red', a(2).name='blue';
#       field : The name of the field which is searched, for example 'name'
#       value : The search value, for example 'blue'
    
    #  outputs,
#       index : The Struct index which match the search
    
    
    # Example,
    
    # a(1).name='blue';
# a(1).index=0;
# a(1).val='g';
    
    # a(2).name='red';
# a(2).index=1;
# a(2).val=[1 0];
    
    # a(3).name='green';
# a(3).index=2;
# a(3).val='g';
    
    # a(4).name='black';
# a(4).index=3;
# a(4).val=[0 0 0];
    
    # a(5).name='yellow';
# a(5).index=NaN;
# a(5).val=[0 1 1];
    
    # a(6).name='orange';
# a(6).index=[];
# a(6).val=[1 1 0];
    
    # a(7).name='brown';
# a(7).index=6;
# a(7).val={'12'};
    
    # a(8).name='white';
# a(8).index=7;
# a(8).val.x=1;
    
    # a(8).name='purple';
# a(8).index=8;
# a(8).val.child.value=2;
    
    # index=structfind(a,'name','red');
# disp(['index : ' num2str(index)])
    
    # index=structfind(a,'index',1);
# disp(['index : ' num2str(index)])
    
    # index=structfind(a,'val',[0 0 0]);
# disp(['index : ' num2str(index)])
    
    # index=structfind(a,'val','g');
# disp(['index : ' num2str(index)])
    
    # index=structfind(a,'index',NaN);
# disp(['index : ' num2str(index)])
    
    # index=structfind(a,'index',[]);
# disp(['index : ' num2str(index)])
    
    # index=structfind(a,'val',{'12'});
# disp(['index : ' num2str(index)])
    
    # index=structfind(a,'val.child.value',2);
# disp(['index : ' num2str(index)])
    
    # Function is written by D.Kroon University of Twente (December 2010)
# We don't compare structs
    if (isstruct(value)):
        error('structfind:inputs','search value can not be a struct')
    
    # Stop if field doesn't exist
    if (logical_not(isfield(a,field))):
        index=find(arrayfun(lambda x=None: (cmp(x,field,value)),a,'uniformoutput',true))
# structfind.m:84
    else:
        index=find(arrayfun(lambda x=None: (cmp(x,field,value)),a,'uniformoutput',true))
# structfind.m:86
    
    
@function
def cmp(x=None,field=None,value=None,*args,**kwargs):
    varargin = cmp.varargin
    nargin = cmp.nargin

    check=copy(false)
# structfind.m:89
    if (isfield(x,field)):
        # Simple field like x.tag
        x=getattr(x,(field))
# structfind.m:92
    else:
        # Complex field like x.tag.child.value
        in_=find(field == '.')
# structfind.m:95
        s=concat([1,in_ + 1])
# structfind.m:96
        e=concat([in_ - 1,length(field)])
# structfind.m:96
        for i in arange(1,length(s)).reshape(-1):
            fieldt=field(arange(s(i),e(i)))
# structfind.m:98
            if (isfield(x,fieldt)):
                x=getattr(x,(fieldt))
# structfind.m:100
            else:
                return check
    
    # We don't compare structs
    if (isstruct(x)):
        return check
    
    # Values can only be equal, if they equal in length
    if (length(x) == length(value)):
        # This part compares the NaN values
        if ((logical_not(iscell(x))) and (logical_not(iscell(value))) and any(isnan(value))):
            checkv=isnan(value)
# structfind.m:112
            checkx=isnan(x)
# structfind.m:112
            if (logical_not(all(checkx == checkv))):
                return check
            x[checkx]=0
# structfind.m:114
            value[checkv]=0
# structfind.m:114
        # This part compares for both string as numerical values
        if (iscell(x) or iscell(value)):
            check=all(strcmp(x,value))
# structfind.m:118
        else:
            check=all(x == value)
# structfind.m:120
    