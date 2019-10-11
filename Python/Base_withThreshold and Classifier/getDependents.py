# Generated with SMOP  0.41
from libsmop import *
# getDependents.m

    
@function
def getDependents(script=None,*args,**kwargs):
    varargin = getDependents.varargin
    nargin = getDependents.nargin

    # put dependents into folder.
    
    file,path=uigetfile(nargout=2)
# getDependents.m:5
    fList,__=matlab.codetools.requiredFilesAndProducts(strcat(path,file),nargout=2)
# getDependents.m:6
    # folder
    depFolder=uigetdir()
# getDependents.m:9
    for f in arange(1,length(fList)).reshape(-1):
        copyfile(fList[f],depFolder)
    
    ##
    
    # also copy dlls and const file
    copyfile(strcat(path,'\user32.dll'),depFolder)
    copyfile(strcat(path,'\user32_thunk_pcwin64.dll'),depFolder)
    copyfile(strcat(path,'\constFile.txt'),depFolder)