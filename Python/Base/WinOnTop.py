# Generated with SMOP  0.41
from libsmop import *
# WinOnTop.m

    
@function
def WinOnTop(figureHandle=None,isOnTop=None,*args,**kwargs):
    varargin = WinOnTop.varargin
    nargin = WinOnTop.nargin

    #WINONTOP allows to trigger figure's "Always On Top" state
    
    ## INPUT ARGUMENTS:
    
    # # figureHandle - Matlab's figure handle, scalar
# # isOnTop      - logical scalar or empty array
    
    
    ## USAGE:
    
    # * WinOnTop( hfigure, true );      - switch on  "always on top"
# * WinOnTop( hfigure, false );     - switch off "always on top"
# * WinOnTop( hfigure );            - equal to WinOnTop( hfigure,true);
# * WinOnTop();                     - equal to WinOnTop( gcf, true);
# * WasOnTop = WinOnTop(...);       - returns boolean value "if figure WAS on top"
# * isOnTop = WinOnTop(hfigure,[])  - get "if figure is on top" property
    
    
    ## LIMITATIONS:
    
    # * java enabled
# * figure must be visible
# * figure's "WindowStyle" should be "normal"
# * figureHandle should not be casted to double, if using HG2 (R2014b+)
    
    
    # Written by Igor
# i3v@mail.ru
    
    # 2013.06.16 - Initial version
# 2013.06.27 - removed custom "ishandle_scalar" function call
# 2015.04.17 - adapted for changes in matlab graphics system (since R2014b)
# 2016.05.21 - another ishg2() checking mechanism 
# 2016.09.24 - fixed IsOnTop vs isOnTop bug
    
    ## Parse Inputs
    
    if logical_not(exist('figureHandle','var')):
        figureHandle=copy(gcf)
# WinOnTop.m:39
    
    assert_(isscalar(figureHandle) and ishandle(figureHandle) and strcmp(get(figureHandle,'Type'),'figure'),'WinOnTop:Bad_figureHandle_input','%s','Provided figureHandle input is not a figure handle')
    assert_(strcmp('on',get(figureHandle,'Visible')),'WinOnTop:FigInisible','%s','Figure Must be Visible')
    assert_(strcmp('normal',get(figureHandle,'WindowStyle')),'WinOnTop:FigWrongWindowStyle','%s','WindowStyle Must be Normal')
    if logical_not(exist('isOnTop','var')):
        isOnTop=copy(true)
# WinOnTop.m:62
    
    assert_(islogical(isOnTop) and isscalar(isOnTop) or isempty(isOnTop),'WinOnTop:Bad_isOnTop_input','%s','Provided isOnTop input is neither boolean, nor empty')
    ## Pre-checks
    
    error(javachk('swing',mfilename))
    
    
    ## Action
    
    # Flush the Event Queue of Graphic Objects and Update the Figure Window.
    drawnow('expose')
    warnStruct=warning('off','MATLAB:HandleGraphics:ObsoletedProperty:JavaFrame')
# WinOnTop.m:84
    jFrame=get(handle(figureHandle),'JavaFrame')
# WinOnTop.m:85
    warning(warnStruct.state,'MATLAB:HandleGraphics:ObsoletedProperty:JavaFrame')
    drawnow
    if ishg2(figureHandle):
        jFrame_fHGxClient=jFrame.fHG2Client
# WinOnTop.m:92
    else:
        jFrame_fHGxClient=jFrame.fHG1Client
# WinOnTop.m:94
    
    wasOnTop=jFrame_fHGxClient.getWindow.isAlwaysOnTop
# WinOnTop.m:98
    if logical_not(isempty(isOnTop)):
        jFrame_fHGxClient.getWindow.setAlwaysOnTop(isOnTop)
    
    return wasOnTop
    
if __name__ == '__main__':
    pass
    
    
@function
def ishg2(figureHandle=None,*args,**kwargs):
    varargin = ishg2.varargin
    nargin = ishg2.nargin

    # There's a detailed discussion, how to check "if using HG2" here:
# http://www.mathworks.com/matlabcentral/answers/136834-determine-if-using-hg2
# however, it looks like there's no perfect solution.
    
    # This approach, suggested by Cris Luengo:
# http://www.mathworks.com/matlabcentral/answers/136834#answer_156739
# should work OK, assuming user is NOT passing a figure handle, casted to
# double, like this:
    
    #   hf=figure();
#   WinOnTop(double(hf));
    
    tf=isa(figureHandle,'matlab.ui.Figure')
# WinOnTop.m:121
    return tf
    
if __name__ == '__main__':
    pass
    