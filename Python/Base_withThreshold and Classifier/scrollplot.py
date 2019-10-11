# Generated with SMOP  0.41
from libsmop import *
# scrollplot.m

    
@function
def scrollplot(varargin=None,*args,**kwargs):
    varargin = scrollplot.varargin
    nargin = scrollplot.nargin

    #SCROLLPLOT add scroll sub-window to the supplied plot handle
    
    #   scrollplot adds a scroll sub-window to any supplied plot handle(s).
#   The user may specify initial view window parameters or use defaults.
#   Dragging the side-bars or central patch modifies the respective parent
#   axes limits interactively. Conversely, modifying the parent axes
#   limits (with zoom, pan or programatically) modifies the corresponding
#   scroll patch(es) accordingly. Works ok with log and reverse axes.
#   Both X & Y scrolling are possible. Custom properties provide access to
#   the scroll axes, central patch and side-bars, for user customizations.
    
    #   Syntax:
#     scrollHandles = scrollplot(plotHandles, propName,propValue,...)
    
    #   scrollplot(plotHandles) adds a scroll sub-window to the supplied
#   plotHandles using default property values (see below).
#   plotHandles may be any combination of axes and line/data handles.
#   If plotHandles is not supplied then the current axes (<a href="matlab:help gca">gca</a>) is used.
    
    #   scrollplot(..., propName,propValue, ...) sets the property value(s)
#   for the initial scroll view window. Property specification order does
#   not matter. The following properties are supported (case-insensitive):
#     - 'Axis'       : string (default = 'X'; accepted values: 'X','Y','XY')
#     - 'Min'        : number (default = minimal value of actual plot data)
#                      sets the same value for both 'MinX' & 'MinY'
#     - 'Max'        : number (default = maximal value of actual plot data)
#                      sets the same value for both 'MaxX' & 'MaxY'
#     - 'MinX','MinY': number (same as 'Min', but only for X or Y axis)
#     - 'MaxX','MaxY': number (same as 'Max', but only for X or Y axis)
#     - 'WindowSize' : number (default = entire range  of actual plot data)
#                      sets the same value for 'WindowSizeX' & 'WindowSizeY'
#     - 'WindowSizeX': number (same as 'WindowSize' but only for X axis)
#     - 'WindowSizeY': number (same as 'WindowSize' but only for Y axis)
    
    #   scrollHandles = scrollplot(...) returns handle(s) to the scroll axes.
#   The returned handles are regular axes with a few additional read-only
#   properties:
#     - 'ScrollSideBarHandles' - array of 2 handles to the scroll side-bars
#     - 'ScrollPatchHandle' - handle to the central scroll patch
#     - 'ScrollAxesHandle'  - handle to the scroll axes =double(scrollHandles)
#     - 'ParentAxesHandle'  - handle to the parent axes
#     - 'ScrollMin'         - number
#     - 'ScrollMax'         - number
    
    #   Examples:
#     scrollplot;  # add scroll sub-window to the current axes (gca)
#     scrollplot(plot(xdata,ydata), 'WindowSize',50); # plot with initial zoom
#     scrollplot('Min',20, 'windowsize',70); # add x-scroll to current axes
#     scrollplot([h1,h2], 'axis','xy'); # scroll both X&Y of 2 plot axes
#     scrollplot('axis','xy', 'minx',20, 'miny',10); # separate scroll minima
    
    #   Notes:
#     1. Matlab 5: scrollplot might NOT work on Matlab versions earlier than 6 (R12)
#     2. Matlab 6: scrollplot is not interactive in zoom mode (ok in Matlab 7+)
#     3. Matlab 6: warnings are disabled as a side-effect (not in Matlab 7+)
#     4. scrollplot modifies the figure's WindowButtonMotionFcn callback
#     5. scrollplot works on 3D plots, but only X & Y axis are scrollable
    
    #   Warning:
#     This code relies in [small] part on undocumented and unsupported
#     Matlab functionality. It works on Matlab 6+, but use at your own risk!
    
    #   Bugs and suggestions:
#     Please send to Yair Altman (altmany at gmail dot com)
    
    #   Change log:
#     2007-May-13: First version posted on MathWorks file exchange: <a href="http://www.mathworks.com/matlabcentral/fileexchange/loadFile.do?objectId=14984">http://www.mathworks.com/matlabcentral/fileexchange/loadFile.do?objectId=14984</a>
#     2007-May-14: Set focus on parent axes after scroll-axes creation; added special scroll props; allowed 'Axis'='xy'
#     2007-May-15: Added 'MinX' etc. params; clarified error msgs; added 'ParentAxesHandle' special prop; fixed 'xy' bugs
#     2007-Jun-14: Enabled image exploration per suggestion by Joe Lotz; improved log axis-scaling behavior per suggestion by Fredric Moisy; added scroll visibility & deletion handlers; fixed minor error handling bug
#     2010-Nov-04: Minor fix for uitab compatibility suggested by Fabian Hof
#     2013-Jun-28: Support for the upcoming HG2
#     2015-Jul-15: Fixed warning about obsolete JavaFrame; preserved figure visibility; fixed zoom/pan compatibility
#     2015-Jul-16: Fixed custom properties in HG2 (R2014b+); removed reliance on the unsupported setptr function
    
    #   See also:
#     plot, gca
    
    #   Programming notes:
#     1. Listeners are set on parent axes's properties so that whenever
#        any of them (xlim,ylim,parent,units,position) is modified, then
#        so are the corresponding scroll axes properties.
#     2. To bypass the mode managers' (zoom, pan, ...) "hijack" of the
#        WindowButtonUpFcn callback, we use the non-supported JavaFrame's
#        AxisComponent MouseReleasedCallback: this doesn't work in Matlab 6
#        so scrollplot is non-interactive in Matlab 6 during zoom mode.
#     3. To bypass the mode managers over the scroll axes (to ignore zoom/
#        pan), we use the little-known 'ButtonDownFilter' mode property.
#     4. The special read-only properties in the returned scrollHandles are
#        not viewable (only accessible) in the regular axes handle, only
#        in the handle(scrollHandles). Therefore, the latter form is returned.
#        If you need the regular (numeric) form, use either double(scrollHandles)
#        or the new 'ScrollAxesHandle' read-only prop.
    
    # License to use and modify this code is granted freely without warranty to all, as long as the original author is
# referenced and attributed as such. The original author maintains the right to be solely associated with this work.
    
    # Programmed and Copyright by Yair M. Altman: altmany(at)gmail.com
# $Revision: 1.7 $  $Date: 2015/07/16 12:22:32 $
    
    try:
        # Note: on some systems with Matlab 6, an OpenGL warning is displayed due to semi-
        # transparent scroll patch. This may be safely ignored. Unfortunately, specific warning
        # disabling was not yet available in Matlab 6 so we must turn off all warnings...
        v=copy(version)
# scrollplot.m:106
        if v(1) <= '6':
            warning('off')
        else:
            # Temporarily turn off log-axis warnings
            oldWarn=warning('off','MATLAB:Axes:NegativeDataInLogAxis')
# scrollplot.m:111
        # Args check
        plotHandles,pvPairs=parseparams(varargin,nargout=2)
# scrollplot.m:115
        if iscell(plotHandles):
            plotHandles=concat([plotHandles[arange()]])
# scrollplot.m:117
        if isempty(plotHandles):
            plotHandles=copy(gca)
# scrollplot.m:120
        else:
            plotHandles=ravel(plotHandles)
# scrollplot.m:122
        # Ensure that all supplied handles are valid HG handles
        if logical_or(isempty(plotHandles),logical_not(all(ishandle(plotHandles)))):
            myError('YMA:scrollplot:invalidHandle','invalid plot handle(s) passed to scrollplot')
        # Get the list of axes handles (supplied handles may be axes or axes children)
        validHandles=[]
# scrollplot.m:131
        try:
            for hIdx in arange(1,length(plotHandles)).reshape(-1):
                thisHandle=plotHandles(hIdx)
# scrollplot.m:134
                if logical_not(strcmpi(get(thisHandle,'type'),'axes')):
                    thisHandle=get(thisHandle,'Parent')
# scrollplot.m:136
                if logical_not(strcmpi(get(thisHandle,'type'),'axes')):
                    myError('YMA:scrollplot:invalidHandle','invalid plot handle passed to scrollplot - must be an axes or line/data handle')
                validHandles=concat([validHandles,thisHandle])
# scrollplot.m:141
            validHandles=unique(validHandles)
# scrollplot.m:143
        finally:
            pass
        # Pre-process args necessary for creating the scroll-plots, if supplied
        pvPairs,axName=preProcessArgs(pvPairs,nargout=2)
# scrollplot.m:150
        #try
        scrollplotHandles=handle([])
# scrollplot.m:154
        for hIdx in arange(1,length(validHandles)).reshape(-1):
            # Loop over all requested scroll axes (x,y, or x&y) for this parent axes
            hAx=validHandles(hIdx)
# scrollplot.m:160
            for axisIdx in arange(1,length(axName)).reshape(-1):
                # Add the new scroll plot axes
                h=addScrollPlot(hAx,axName(axisIdx))
# scrollplot.m:163
                try:
                    scrollplotHandles[end() + 1]=h
# scrollplot.m:165
                finally:
                    pass
                # Process args, if supplied
                processArgs(pvPairs,scrollplotHandles(end()))
            # Set the focus on the parent axes
            try:
                # This keeps the figure visibility unchanged
                set(gcf,'CurrentAxes',hAx)
            finally:
                pass
        #catch
            # Probably not a valid axes handle
            #myError('YMA:scrollplot:invalidHandle','invalid plot handle(s) passed to scrollplot - must be an axes or line/data handle');
        #end
        # If return scrollHandles was requested
        if nargout:
            # Return the list of all scroll handles
            scrollHandles=copy(scrollplotHandles)
# scrollplot.m:191
    finally:
        pass
    
    # Restore original warnings (if available/possible)
    try:
        warning(oldWarn)
    finally:
        pass
    
    #end  # scrollplot  ##ok for Matlab 6 compatibility
    
    ## Set-up a new scroll sub-plot window to the supplied axes handle
    
@function
def addScrollPlot(hAx=None,axName=None,*args,**kwargs):
    varargin = addScrollPlot.varargin
    nargin = addScrollPlot.nargin

    # Before modifying the original axes position, we must fix the labels (esp. xlabel)
    hLabel=get(hAx,concat([axName,'Label']))
# scrollplot.m:241
    set(hLabel,'units','normalized')
    
    axPos=get(hAx,'position')
# scrollplot.m:245
    axVis=get(hAx,'visible')
# scrollplot.m:246
    axUnits=get(hAx,'units')
# scrollplot.m:247
    scaleStr=concat([axName,'Scale'])
# scrollplot.m:248
    dirStr=concat([axName,'Dir'])
# scrollplot.m:249
    limStr=concat([axName,'Lim'])
# scrollplot.m:250
    if strcmpi(axName,'x'):
        newScrollPos=multiply(axPos,concat([1,1,1,0.1]))
# scrollplot.m:252
        newPlotPos=multiply(axPos,concat([1,1,1,0.8])) + concat([0,dot(0.2,axPos(4)),0,0])
# scrollplot.m:253
        specialStr=cellarray(['YTick',[]])
# scrollplot.m:254
        colStr='YColor'
# scrollplot.m:255
        rotation=0
# scrollplot.m:256
    else:
        newScrollPos=concat([axPos(1) + dot(axPos(3),0.85),axPos(2),dot(axPos(3),0.1),axPos(4)])
# scrollplot.m:258
        newPlotPos=multiply(axPos,concat([1,1,0.8,1]))
# scrollplot.m:259
        specialStr=cellarray(['XTick',[],'YAxisLocation','right'])
# scrollplot.m:260
        colStr='XColor'
# scrollplot.m:261
        rotation=90
# scrollplot.m:262
    
    hScroll=axes('units',axUnits,'Parent',get(hAx,'Parent'),'position',newScrollPos,'visible',axVis,scaleStr,get(hAx,scaleStr),dirStr,get(hAx,dirStr),'NextPlot','add','Box','off',specialStr[arange()],'FontSize',7,'Tag','scrollAx','UserData',axName,'DeleteFcn',deleteScrollAx)
# scrollplot.m:264
    GRAY=dot(0.8,concat([1,1,1]))
# scrollplot.m:265
    try:
        bgColor=get(get(hAx,'parent'),'Color')
# scrollplot.m:267
        set(hScroll,colStr,bgColor)
    finally:
        pass
    
    #axis(hScroll, 'off');
    set(hAx,'position',newPlotPos)
    
    setappdata(hScroll,'parent',hAx)
    
    # Note: use any axes child xdata to set the scroll limits, but
    # ^^^^  only plot line children (not scatter/bar/polar etc)
    axLines=get(hAx,'children')
# scrollplot.m:282
    
    lim=get(hAx,limStr)
# scrollplot.m:284
    if isinf(lim(1)):
        lim[1]=+ inf
# scrollplot.m:285
    
    if isinf(lim(2)):
        lim[2]=- inf
# scrollplot.m:286
    
    for lineIdx in arange(1,length(axLines)).reshape(-1):
        try:
            hLine=axLines(lineIdx)
# scrollplot.m:289
            xdata=get(hLine,'XData')
# scrollplot.m:290
            ydata=get(hLine,'YData')
# scrollplot.m:291
            try:
                name=get(hLine,'DisplayName')
# scrollplot.m:293
            finally:
                pass
            if strcmpi(axName,'x'):
                data=xdata(1,arange())
# scrollplot.m:298
            else:
                data=ydata(1,arange())
# scrollplot.m:298
            lim=concat([min(lim(1),min(data)),max(lim(2),max(data))])
# scrollplot.m:299
            linType=get(hLine,'type')
# scrollplot.m:300
            if strcmpi(linType,'line'):
                # Add plot line child if and only if it's a line
                lineColor=copy(GRAY)
# scrollplot.m:303
                hLine2=plot(xdata,ydata,'Parent',hScroll,'color',lineColor,'tag','scrollDataLine','HitTest','off')
# scrollplot.m:304
                if logical_not(isempty(name)):
                    set(hLine2,'DisplayName',name)
                # 2007-Jun-14: Enabled image exploration per suggestion by Joe Lotz
            else:
                if strcmpi(linType,'image'):
                    # Add miniature version of the main image
                    hLine2=image(get(hLine,'CData'),'Parent',hScroll)
# scrollplot.m:311
                    set(hScroll,'YDir','Reverse','XLim',get(hLine,'XData'),'YLim',get(hLine,'YData'))
        finally:
            pass
    
    if lim(1) > lim(2):
        curLim=get(hScroll,limStr)
# scrollplot.m:319
        if isinf(lim(1)):
            lim[1]=curLim(1)
# scrollplot.m:320
        if isinf(lim(2)):
            lim[2]=curLim(2)
# scrollplot.m:321
    
    if logical_and(logical_not(isempty(axLines)),lim(1)) < lim(2):
        set(hScroll,limStr,lim)
    
    # Get the figure handle
    hFig=ancestor(hAx,'figure')
# scrollplot.m:328
    
    set(hFig,'DoubleBuffer','on')
    
    # Note: this is determined by the first invocation, so ensure we're the first...
    axisComponent=getAxisComponent(hFig)
# scrollplot.m:335
    
    # Set the scroll handle-bars
    xlim=get(hScroll,'XLim')
# scrollplot.m:338
    ylim=get(hScroll,'YLim')
# scrollplot.m:339
    hPatch=patch(xlim(concat([1,1,2,2])),ylim(concat([1,2,2,1])),'b','FaceAlpha',0.15,'EdgeColor','w','EdgeAlpha',0.15,'ButtonDownFcn',mouseDownCallback,'tag','scrollPatch','userdata',axName)
# scrollplot.m:340
    
    commonProps=cellarray(['Parent',hScroll,'LineWidth',3,'ButtonDownFcn',mouseDownCallback,'tag','scrollBar'])
# scrollplot.m:341
    smallDelta=dot(0.01,diff(lim))
# scrollplot.m:342
    
    if strcmpi(axName,'x'):
        hBars[1]=plot(xlim(concat([1,1])),ylim,'-b',commonProps[arange()])
# scrollplot.m:344
        hBars[2]=plot(xlim(concat([2,2])),ylim,'-b',commonProps[arange()])
# scrollplot.m:345
    else:
        hBars[1]=plot(xlim,ylim(concat([1,1])) + smallDelta,'-b',commonProps[arange()])
# scrollplot.m:347
        hBars[2]=plot(xlim,ylim(concat([2,2])) - smallDelta,'-b',commonProps[arange()])
# scrollplot.m:348
    
    try:
        set(hBars(1),'DisplayName','Min')
        set(hBars(2),'DisplayName','Max')
    finally:
        pass
    
    # TODO: maybe add a blue diamond or a visual handle in center of hBars?
    set(hScroll,limStr,lim + dot(smallDelta,concat([- 1.2,1.2])))
    
    msg=cellarray(['drag blue side-bars to zoom','drag central patch to pan'])
# scrollplot.m:360
    xText=getCenterCoord(hScroll,'x')
# scrollplot.m:361
    yText=getCenterCoord(hScroll,'y')
# scrollplot.m:362
    hText=text(xText,yText,msg,'Color','r','Rotation',rotation,'HorizontalAlignment','center','FontSize',9,'FontWeight','bold','HitTest','off','tag','scrollHelp')
# scrollplot.m:363
    
    hMenu=copy(uicontextmenu)
# scrollplot.m:364
    set(hScroll,'UIContextMenu',hMenu)
    uimenu(hMenu,'Label',msg[1],'Callback',moveCursor,'UserData',hBars(2))
    uimenu(hMenu,'Label',msg[2],'Callback',moveCursor,'UserData',hPatch)
    
    winFcn=get(hFig,'WindowButtonMotionFcn')
# scrollplot.m:370
    if logical_and(logical_and(logical_not(isempty(winFcn)),logical_not(isequal(winFcn,mouseMoveCallback))),(logical_or(logical_not(iscell(winFcn)),logical_not(isequal(winFcn[1],mouseMoveCallback))))):
        setappdata(hFig,'scrollplot_oldButtonMotionFcn',winFcn)
    
    set(hFig,'WindowButtonMotionFcn',mouseMoveCallback)
    
    oldPos=get(hLabel,'position')
# scrollplot.m:377
    if strcmpi(axName,'x'):
        if logical_and(logical_not(isempty(oldPos)),oldPos(2)) < 0:
            # Only fix if the X label is on the bottom (usually yes)
            set(hLabel,'position',oldPos - concat([0,0.2 / 0.8,0]))
    else:
        if logical_and(logical_not(isempty(oldPos)),oldPos(1)) > 0:
            # Only fix if the Y label is on the right side (usually not)
            set(hLabel,'position',oldPos + concat([0.2 / 0.8,0,0]))
    
    # Add property listeners
    listenedPropNames=cellarray(['XLim','YLim','XDir','YDir','XScale','YScale','Position','Units','Parent'])
# scrollplot.m:391
    listeners=addPropListeners(hFig,hAx,hScroll,hPatch,hBars,listenedPropNames)
# scrollplot.m:392
    setappdata(hScroll,'scrollplot_listeners',listeners)
    
    # Add special properties
    addSpecialProps(hAx,hScroll,hPatch,hBars,axName)
    
    hScroll=handle(hScroll)
# scrollplot.m:399
    return hScroll
    
    #end  # addScrollPlot  ##ok for Matlab 6 compatibility
    
    ## Add parent axes listener
    
@function
def addPropListeners(hFig=None,hAx=None,hScroll=None,hPatch=None,hBars=None,propNames=None,*args,**kwargs):
    varargin = addPropListeners.varargin
    nargin = addPropListeners.nargin

    # Listeners on parent axes properties
    hhAx=handle(hAx)
# scrollplot.m:406
    for propIdx in arange(1,length(propNames)).reshape(-1):
        propName=propNames[propIdx]
# scrollplot.m:408
        callback=cellarray([parentAxesChanged,hFig,hAx,hPatch,hBars,propName])
# scrollplot.m:409
        prop=findprop(hhAx,propName)
# scrollplot.m:410
        try:
            listeners[propIdx]=handle.listener(hhAx,prop,'PropertyPostSet',callback)
# scrollplot.m:412
        finally:
            pass
    
    # Listeners on scroll axes properties
    hhScroll=handle(hScroll)
# scrollplot.m:420
    prop=findprop(hhScroll,'Visible')
# scrollplot.m:421
    try:
        listeners[end() + 1]=handle.listener(hhScroll,prop,'PropertyPostSet',cellarray([updateParentPos,hScroll]))
# scrollplot.m:423
    finally:
        pass
    
    #end  # addPropListeners  ##ok for Matlab 6 compatibility
    
    ## Add special scrollplot properties to the hScroll axes
    
@function
def addSpecialProps(hAx=None,hScroll=None,hPatch=None,hBars=None,axName=None,*args,**kwargs):
    varargin = addSpecialProps.varargin
    nargin = addSpecialProps.nargin

    try:
        hhScroll=handle(hScroll)
# scrollplot.m:432
        addNewProp(hhScroll,'ParentAxesHandle',hAx,1)
        addNewProp(hhScroll,'ScrollAxesHandle',double(hScroll),1)
        addNewProp(hhScroll,'ScrollPatchHandle',hPatch,1)
        addNewProp(hhScroll,'ScrollSideBarHandles',hBars,1)
        dataStr=concat([axName,'Data'])
# scrollplot.m:441
        addNewProp(hhScroll,'ScrollMin',unique(get(hBars(1),dataStr)),1)
        addNewProp(hhScroll,'ScrollMax',unique(get(hBars(2),dataStr)),1)
    finally:
        pass
    
    #end  # addSpecialProps  ##ok for Matlab 6 compatibility
    
    ## Add new property to supplied handle
    
@function
def addNewProp(hndl=None,propName=None,initialValue=None,readOnlyFlag=None,getFunc=None,setFunc=None,*args,**kwargs):
    varargin = addNewProp.varargin
    nargin = addNewProp.nargin

    try:
        sp=schema.prop(hndl,propName,'mxArray')
# scrollplot.m:452
        set(hndl,propName,initialValue)
        if nargin > logical_and(logical_and(3,logical_not(isempty(readOnlyFlag))),readOnlyFlag):
            set(sp,'AccessFlags.PublicSet','off')
        if nargin > logical_and(4,logical_not(isempty(getFunc))):
            set(sp,'GetFunction',getFunc)
        if nargin > logical_and(5,logical_not(isempty(setFunc))):
            set(sp,'SetFunction',setFunc)
    finally:
        pass
    
    #end  # addNewProp  ##ok for Matlab 6 compatibility
    
    ## Callback for getting side-bar value
    
@function
def getBarVal(object=None,propValue=None,varargin=None,*args,**kwargs):
    varargin = getBarVal.varargin
    nargin = getBarVal.nargin

    propValue=unique(get(varargin[arange()]))
# scrollplot.m:480
    #end  # getBarVal  ##ok for Matlab 6 compatibility
    
    ## Pre-process args necessary for creating the scroll-plots, if supplied
    
@function
def preProcessArgs(pvPairs=None,*args,**kwargs):
    varargin = preProcessArgs.varargin
    nargin = preProcessArgs.nargin

    # Default axes is 'X'
    axName='x'
# scrollplot.m:486
    
    if logical_and(logical_and(logical_not(isempty(pvPairs)),ischar(pvPairs[end()])),any(strcmpi(pvPairs[end()],cellarray(['axis','axes'])))):
        myError('YMA:scrollplot:invalidProperty','No data specified for scrollplot property 'Axis'')
    
    # Loop over all supplied P-V pairs to pre-process the parameters
    idx=1
# scrollplot.m:494
    while idx < length(pvPairs):

        paramName=pvPairs[idx]
# scrollplot.m:496
        if logical_not(ischar(paramName)):
            idx=idx + 1
# scrollplot.m:497
            continue
        if cellarray(['axis','axes']) == lower(paramName):
            axName=pvPairs[idx + 1]
# scrollplot.m:502
            if logical_or(logical_not(ischar(axName)),logical_not(any(strcmpi(axName,cellarray(['x','y','xy','yx']))))):
                myError('YMA:scrollplot:invalidProperty','Invalid scrollplot 'Axis' property value: only 'x','y' & 'xy' are accepted')
            # Remove from the PV pairs list and move on
            axName=lower(axName)
# scrollplot.m:508
            pvPairs[arange(idx,idx + 1)]=[]
# scrollplot.m:509
        else:
            # Skip...
            idx=idx + 1
# scrollplot.m:514

    
    #end  # preProcessArgs  ##ok for Matlab 6 compatibility
    
    ## Process P-V argument pairs
    
@function
def processArgs(pvPairs=None,hScroll=None,*args,**kwargs):
    varargin = processArgs.varargin
    nargin = processArgs.nargin

    try:
        minLim=[]
# scrollplot.m:522
        maxLim=[]
# scrollplot.m:523
        hScroll=double(hScroll)
# scrollplot.m:524
        axName=get(hScroll,'userdata')
# scrollplot.m:525
        if strcmpi(axName,'x'):
            otherAxName='y'
# scrollplot.m:527
        else:
            otherAxName='x'
# scrollplot.m:529
        dataStr=concat([axName,'Data'])
# scrollplot.m:531
        limStr=concat([axName,'Lim'])
# scrollplot.m:532
        while logical_not(isempty(pvPairs)):

            # Ensure basic format is valid
            paramName=''
# scrollplot.m:535
            if logical_not(ischar(pvPairs[1])):
                myError('YMA:scrollplot:invalidProperty','Invalid property passed to scrollplot')
            else:
                if length(pvPairs) == 1:
                    myError('YMA:scrollplot:invalidProperty',concat(['No data specified for property '',pvPairs[1],''']))
            # Process parameter values
            paramName=pvPairs[1]
# scrollplot.m:543
            paramValue=pvPairs[2]
# scrollplot.m:544
            pvPairs[arange(1,2)]=[]
# scrollplot.m:545
            hScrollBars=unique(findall(hScroll,'tag','scrollBar'))
# scrollplot.m:546
            hScrollPatches=unique(findall(hScroll,'tag','scrollPatch'))
# scrollplot.m:547
            if cellarray(['min',concat(['min',axName])]) == lower(paramName):
                set(hScrollBars(arange(1,end(),2)),dataStr,paramValue(concat([1,1])))
                for patchIdx in arange(1,length(hScrollPatches)).reshape(-1):
                    thisPatch=hScrollPatches(patchIdx)
# scrollplot.m:552
                    data=get(thisPatch,dataStr)
# scrollplot.m:553
                    if strcmpi(axName,'x'):
                        set(thisPatch,dataStr,concat([[paramValue(concat([[1],[1]]))],[data(concat([4,4]))]]))
                    else:
                        set(thisPatch,dataStr,concat([[paramValue(1)],[data(concat([2,2]))],[paramValue(1)]]))
                    # Update the parent axes with the new limit
                    hAx=getappdata(get(thisPatch,'Parent'),'parent')
# scrollplot.m:561
                    lim=get(hAx,limStr)
# scrollplot.m:562
                    set(hAx,limStr,concat([paramValue,lim(2)]))
                minLim=copy(paramValue)
# scrollplot.m:565
            else:
                if cellarray(['max',concat(['max',axName])]) == lower(paramName):
                    set(hScrollBars(arange(2,end(),2)),dataStr,paramValue(concat([1,1])))
                    for patchIdx in arange(1,length(hScrollPatches)).reshape(-1):
                        thisPatch=hScrollPatches(patchIdx)
# scrollplot.m:570
                        data=get(thisPatch,dataStr)
# scrollplot.m:571
                        if strcmpi(axName,'x'):
                            set(thisPatch,dataStr,concat([[data(concat([1,1]))],[paramValue(concat([[1],[1]]))]]))
                        else:
                            set(thisPatch,dataStr,concat([[data(1)],[paramValue(concat([[1],[1]]))],[data(1)]]))
                        # Update the parent axes with the new limit
                        hAx=getappdata(get(thisPatch,'Parent'),'parent')
# scrollplot.m:579
                        lim=get(hAx,limStr)
# scrollplot.m:580
                        set(hAx,limStr,concat([lim(1),paramValue]))
                    maxLim=copy(paramValue)
# scrollplot.m:583
                else:
                    if cellarray(['windowsize',concat(['windowsize',axName])]) == lower(paramName):
                        if isempty(pvPairs):
                            # No min,max after this param, so act based on data so far
                            if logical_not(isempty(minLim)):
                                if logical_and(logical_not(isempty(maxLim)),abs(maxLim - minLim - paramValue(1))) > eps:
                                    myError('YMA:scrollplot:invalidWindowSize','Specified WindowSize value conflicts with earlier values specified for Min,Max')
                                pvPairs=cellarray(['Max',minLim + paramValue(1),pvPairs[arange()]])
# scrollplot.m:592
                            else:
                                if logical_not(isempty(maxLim)):
                                    pvPairs=cellarray(['Min',maxLim - paramValue(1),pvPairs[arange()]])
# scrollplot.m:594
                                else:
                                    # No min,max: act based on actual min for each axes seperately
                                    for scrollIdx in arange(1,length(hScroll)).reshape(-1):
                                        # Update the right side bar
                                        thisScroll=hScroll(scrollIdx)
# scrollplot.m:599
                                        hScrollBars=unique(findall(thisScroll,'tag','scrollBar'))
# scrollplot.m:600
                                        maxLim=get(hScrollBars(1),dataStr) + paramValue(1)
# scrollplot.m:601
                                        set(hScrollBars(2),dataStr,maxLim)
                                        thisPatch=unique(findall(thisScroll,'tag','scrollPatch'))
# scrollplot.m:605
                                        data=get(thisPatch,dataStr)
# scrollplot.m:606
                                        if strcmpi(axName,'x'):
                                            set(thisPatch,dataStr,concat([[data(concat([1,1]))],[maxLim.T]]))
                                        else:
                                            set(thisPatch,dataStr,concat([[data(1)],[maxLim.T],[data(1)]]))
                                        # Finally, update the parent axes with the new limit
                                        hAx=getappdata(thisScroll,'parent')
# scrollplot.m:614
                                        lim=get(hAx,limStr)
# scrollplot.m:615
                                        set(hAx,limStr,concat([lim(1),maxLim(1)]))
                        else:
                            # Push this P-V pair to the end of the params list (after min,max)
                            pvPairs=cellarray([pvPairs[arange()],paramName,paramValue(1)])
# scrollplot.m:621
                        # Not a good idea to let users play with position so easily...
                #case 'position'
                #    set(hScroll, 'position',paramValue);
                    else:
                        if cellarray(['axis','axes']) == lower(paramName):
                            # Do nothing (should never get here: should have been stripped by preProcessArgs()!)
                            pass
                        else:
                            if cellarray([concat(['min',otherAxName]),concat(['max',otherAxName]),concat(['windowsize',otherAxName])]) == lower(paramName):
                                # Do nothing (pass to other axes for processing)
                                pass
                            else:
                                myError('YMA:scrollplot:invalidProperty','Unsupported property')

    finally:
        pass
    
    #end  # processArgs  ##ok for Matlab 6 compatibility
    
    ## Internal error processing
    
@function
def myError(id=None,msg=None,*args,**kwargs):
    varargin = myError.varargin
    nargin = myError.nargin

    v=copy(version)
# scrollplot.m:647
    if (v(1) >= '7'):
        error(id,msg)
    else:
        # Old Matlab versions do not have the error(id,msg) syntax...
        error(msg)
    
    #end  # myError  ##ok for Matlab 6 compatibility
    
    ## Get ancestor figure - used for old Matlab versions that don't have a built-in ancestor()
    
@function
def ancestor(hObj=None,type_=None,*args,**kwargs):
    varargin = ancestor.varargin
    nargin = ancestor.nargin

    if logical_and(logical_not(isempty(hObj)),ishandle(hObj)):
        #if ~isa(handle(hObj),type)  # this is best but always returns 0 in Matlab 6!
        if logical_not(strcmpi(get(hObj,'type'),type_)):
            hObj=ancestor(get(handle(hObj),'parent'),type_)
# scrollplot.m:661
    
    #end  # ancestor  ##ok for Matlab 6 compatibility
    
    ## Helper function to extract first data value(s) from an array
    
@function
def getFirstVals(vals=None,*args,**kwargs):
    varargin = getFirstVals.varargin
    nargin = getFirstVals.nargin

    if isempty(vals):
        data=[]
# scrollplot.m:669
    else:
        if iscell(vals):
            for idx in arange(1,length(vals)).reshape(-1):
                thisVal=vals[idx]
# scrollplot.m:672
                data[idx]=thisVal(1)
# scrollplot.m:673
        else:
            data=vals(arange(),1)
# scrollplot.m:676
    
    #end  # getFirstVal  ##ok for Matlab 6 compatibility
    
    ## Mouse movement outside the scroll patch area
    
@function
def mouseOutsidePatch(hFig=None,inDragMode=None,hAx=None,*args,**kwargs):
    varargin = mouseOutsidePatch.varargin
    nargin = mouseOutsidePatch.nargin

    try:
        # Restore the original figure pointer (probably 'arrow', but not necessarily)
        # On second thought, it should always be 'arrow' since zoom/pan etc. are disabled within hScroll
        #if ~isempty(hAx)
            # Only modify this within hScroll (outside the patch area) - not in other axes
        set(hFig,'Pointer','arrow')
        oldPointer=getappdata(hFig,'scrollplot_oldPointer')
# scrollplot.m:689
        if logical_not(isempty(oldPointer)):
            #set(hFig, oldPointer{:});  # see comment above
            drawnow
            rmappdataIfExists(hFig,'scrollplot_oldPointer')
            if isappdata(hFig,'scrollplot_mouseUpPointer'):
                setappdata(hFig,'scrollplot_mouseUpPointer',oldPointer)
        # Restore the original ButtonUpFcn callback
        if isappdata(hFig,'scrollplot_oldButtonUpFcn'):
            oldButtonUpFcn=getappdata(hFig,'scrollplot_oldButtonUpFcn')
# scrollplot.m:701
            axisComponent=getappdata(hFig,'scrollplot_oldButtonUpObj')
# scrollplot.m:702
            if logical_not(isempty(axisComponent)):
                set(axisComponent,'MouseReleasedCallback',oldButtonUpFcn)
            else:
                set(hFig,'WindowButtonUpFcn',oldButtonUpFcn)
            rmappdataIfExists(hFig,'scrollplot_oldButtonUpFcn')
        # Additional cleanup
        rmappdataIfExists(hFig,'scrollplot_mouseDownPointer')
        if logical_not(inDragMode):
            rmappdataIfExists(hFig,'scrollplot_originalX')
            rmappdataIfExists(hFig,'scrollplot_originalLimits')
    finally:
        pass
    
    #end  # outsideScrollCleanup  ##ok for Matlab 6 compatibility
    
    ## Mouse movement within the scroll patch area
    
@function
def mouseWithinPatch(hFig=None,inDragMode=None,hAx=None,scrollPatch=None,cx=None,isOverBar=None,*args,**kwargs):
    varargin = mouseWithinPatch.varargin
    nargin = mouseWithinPatch.nargin

    try:
        # Separate actions for X,Y scrolling
        axName=get(hAx,'userdata')
# scrollplot.m:727
        if strcmpi(axName,'x'):
            shapeStr='lrdrag'
# scrollplot.m:729
        else:
            shapeStr='uddrag'
# scrollplot.m:731
        dataStr=concat([axName,'Data'])
# scrollplot.m:733
        limStr=concat([axName,'Lim'])
# scrollplot.m:734
        axisComponent=getAxisComponent(hFig)
# scrollplot.m:737
        if logical_not(isempty(axisComponent)):
            winUpFcn=get(axisComponent,'MouseReleasedCallback')
# scrollplot.m:739
        else:
            winUpFcn=get(hFig,'WindowButtonUpFcn')
# scrollplot.m:741
        if logical_or(isempty(winUpFcn),(logical_and(logical_not(isequal(winUpFcn,mouseUpCallback)),(logical_or(logical_not(iscell(winUpFcn)),logical_not(isequal(winUpFcn[1],mouseUpCallback))))))):
            # Set the ButtonUpFcn callbacks
            if logical_not(isempty(winUpFcn)):
                setappdata(hFig,'scrollplot_oldButtonUpFcn',winUpFcn)
                setappdata(hFig,'scrollplot_oldButtonUpObj',axisComponent)
            if logical_not(isempty(axisComponent)):
                set(axisComponent,'MouseReleasedCallback',cellarray([mouseUpCallback,hFig]))
            else:
                oldWarn=warning('off','MATLAB:modes:mode:InvalidPropertySet')
# scrollplot.m:752
                set(hFig,'WindowButtonUpFcn',mouseUpCallback)
                warning(oldWarn)
            # Clear up potential junk that might confuse us later
            if logical_not(inDragMode):
                rmappdataIfExists(hFig,'scrollplot_clickedBarIdx')
        # If this is a drag movement (i.e., mouse button is clicked)
        if inDragMode:
            # Act according to the dragged object
            if isempty(scrollPatch):
                scrollPatch=findobj(hAx,'tag','scrollPatch')
# scrollplot.m:768
            scrollBarIdx=getappdata(hFig,'scrollplot_clickedBarIdx')
# scrollplot.m:770
            scrollBars=sort(findobj(hAx,'tag','scrollBar'))
# scrollplot.m:771
            barsXs=getFirstVals(get(scrollBars,dataStr))
# scrollplot.m:773
            if barsXs(1) > barsXs(2):
                scrollBarIdx=3 - scrollBarIdx
# scrollplot.m:775
                scrollBars=scrollBars(concat([2,1]))
# scrollplot.m:776
            oldPatchXs=get(scrollPatch,dataStr)
# scrollplot.m:778
            axLimits=get(hAx,limStr)
# scrollplot.m:779
            cx=min(max(cx,axLimits(1)),axLimits(2))
# scrollplot.m:780
            if isempty(scrollBarIdx):
                originalX=getappdata(hFig,'scrollplot_originalX')
# scrollplot.m:782
                originalLimits=getappdata(hFig,'scrollplot_originalLimits')
# scrollplot.m:783
                if logical_not(isempty(originalLimits)):
                    allowedDelta=concat([min(0,axLimits(1) - originalLimits(1)),max(0,axLimits(2) - originalLimits(2))])
# scrollplot.m:785
                    deltaX=min(max(cx - originalX,allowedDelta(1)),allowedDelta(2))
# scrollplot.m:786
                    if strcmpi(get(hAx,concat([axName,'Scale'])),'log'):
                        newLimits=10.0 ** (log10(originalLimits) + deltaX)
# scrollplot.m:788
                    else:
                        newLimits=originalLimits + deltaX
# scrollplot.m:790
                    #fprintf('#.3f ',[cx-originalX, deltaX, originalLimits(1), newLimits(1), allowedDelta])
                    #fprintf('\n');
                    if strcmpi(axName,'x'):
                        set(scrollPatch,dataStr,newLimits(concat([1,1,2,2])))
                    else:
                        set(scrollPatch,dataStr,newLimits(concat([1,2,2,1])))
                    set(scrollBars(1),dataStr,newLimits(concat([1,1])))
                    set(scrollBars(2),dataStr,newLimits(concat([2,2])))
                    setappdata(hFig,'scrollplot_originalLimits',newLimits)
                    setappdata(hFig,'scrollplot_originalX',cx)
                    if deltaX != 0:
                        delete(findall(0,'tag','scrollHelp'))
            else:
                if (scrollBarIdx == 1):
                    set(scrollBars(scrollBarIdx),dataStr,concat([cx,cx]))
                    if strcmpi(axName,'x'):
                        set(scrollPatch,dataStr,concat([cx,cx,dot(max(oldPatchXs),concat([1,1]))]))
                    else:
                        set(scrollPatch,dataStr,concat([cx,dot(max(oldPatchXs),concat([1,1])),cx]))
                    delete(findall(0,'tag','scrollHelp'))
                else:
                    set(scrollBars(scrollBarIdx),dataStr,concat([cx,cx]))
                    if strcmpi(axName,'x'):
                        set(scrollPatch,dataStr,concat([dot(min(oldPatchXs),concat([1,1])),cx,cx]))
                    else:
                        set(scrollPatch,dataStr,concat([cx,dot(min(oldPatchXs),concat([1,1])),cx]))
                    delete(findall(0,'tag','scrollHelp'))
            # Modify the parent axes accordingly
            parentAx=getappdata(hAx,'parent')
# scrollplot.m:826
            newXLim=unique(get(scrollPatch,dataStr))
# scrollplot.m:827
            if length(newXLim) == 2:
                if size(newXLim,1) == 2:
                    newXLim=newXLim.T
# scrollplot.m:829
                set(parentAx,limStr,newXLim)
            # Mode managers (zoom/pan etc.) modify the cursor shape, so we need to force ours...
            newPtr=getappdata(hFig,'scrollplot_mouseDownPointer')
# scrollplot.m:834
            if logical_not(isempty(newPtr)):
                setptr(hFig,newPtr)
        else:
            # Modify the cursor shape
            oldPointer=getappdata(hFig,'scrollplot_oldPointer')
# scrollplot.m:842
            if isempty(oldPointer):
                # Preserve original pointer shape for future use
                setappdata(hFig,'scrollplot_oldPointer',getptr(hFig))
            if isOverBar:
                setptr(hFig,shapeStr)
                setappdata(hFig,'scrollplot_mouseDownPointer',shapeStr)
            else:
                setptr(hFig,'hand')
                setappdata(hFig,'scrollplot_mouseDownPointer','closedhand')
        drawnow
    finally:
        pass
    
    #end  # mouseWithinPatch  ##ok for Matlab 6 compatibility
    
    ## Mouse movement callback function
    
@function
def mouseMoveCallback(varargin=None,*args,**kwargs):
    varargin = mouseMoveCallback.varargin
    nargin = mouseMoveCallback.nargin

    try:
        try:
            # Temporarily turn off log-axis warnings
            oldWarn=warning('off','MATLAB:Axes:NegativeDataInLogAxis')
# scrollplot.m:867
        finally:
            pass
        # Get the figure's current axes
        hFig=copy(gcbf)
# scrollplot.m:873
        if logical_or(isempty(hFig),logical_not(ishandle(hFig))):
            return
        #hAx = get(hFig,'currentAxes');
        hAx=getCurrentScrollAx(hFig)
# scrollplot.m:876
        inDragMode=isappdata(hFig,'scrollplot_clickedBarIdx')
# scrollplot.m:877
        if isappdata(hFig,'scrollBar_inProgress'):
            return
        # Fix case of Mode Managers (pan, zoom, ...)
        try:
            modeMgr=get(hFig,'ModeManager')
# scrollplot.m:884
            hMode=modeMgr.CurrentMode
# scrollplot.m:885
            set(hMode,'ButtonDownFilter',shouldModeBeInactiveFcn)
        finally:
            pass
        # If mouse pointer is not currently over any scroll axes
        if isempty(hAx):
            # Perform cleanup
            mouseOutsidePatch(hFig,inDragMode,hAx)
        else:
            # Check whether the curser is over any side bar
            scrollPatch=findobj(hAx,'tag','scrollPatch')
# scrollplot.m:898
            isOverBar=0
# scrollplot.m:899
            cx=[]
# scrollplot.m:900
            if logical_not(isempty(scrollPatch)):
                scrollPatch=scrollPatch(1)
# scrollplot.m:902
                axName=get(hAx,'userdata')
# scrollplot.m:903
                cp=get(hAx,'CurrentPoint')
# scrollplot.m:904
                cx=cp(1,1)
# scrollplot.m:905
                cy=cp(1,2)
# scrollplot.m:906
                xlim=get(hAx,'Xlim')
# scrollplot.m:907
                ylim=get(hAx,'Ylim')
# scrollplot.m:908
                limits=get(hAx,concat([axName,'Lim']))
# scrollplot.m:909
                barXs=unique(get(scrollPatch,concat([axName,'Data'])))
# scrollplot.m:910
                if strcmpi(get(hAx,concat([axName,'Scale'])),'log'):
                    fuzz=dot(0.01,diff(log(abs(limits))))
# scrollplot.m:912
                    barXs=log10(barXs)
# scrollplot.m:913
                    if strcmpi(axName,'x'):
                        cx=log10(cx)
# scrollplot.m:915
                    else:
                        cy=log10(cy)
# scrollplot.m:917
                else:
                    fuzz=dot(0.01,diff(limits))
# scrollplot.m:920
                if isempty(barXs):
                    return
                #disp(abs(cy-barXs)')
                if strcmpi(axName,'x'):
                    inXTest=logical_and(any(barXs - fuzz < cx),any(cx < barXs + fuzz))
# scrollplot.m:925
                    inYTest=logical_and((ylim(1) < cy),(cy < ylim(2)))
# scrollplot.m:926
                    isOverBar=any(abs(cx - barXs) < fuzz)
# scrollplot.m:927
                else:
                    inXTest=logical_and((xlim(1) < cx),(cx < xlim(2)))
# scrollplot.m:929
                    inYTest=logical_and(any(barXs - fuzz < cy),any(cy < barXs + fuzz))
# scrollplot.m:930
                    isOverBar=any(abs(cy - barXs) < fuzz)
# scrollplot.m:931
                    cx=copy(cy)
# scrollplot.m:932
                scrollPatch=scrollPatch(logical_and(inXTest,inYTest))
# scrollplot.m:934
                if strcmpi(get(hAx,concat([axName,'Scale'])),'log'):
                    cx=10 ** cx
# scrollplot.m:936
            # From this moment on, don't allow any interruptions
            setappdata(hFig,'scrollBar_inProgress',1)
            if logical_or(logical_not(isempty(scrollPatch)),inDragMode):
                mouseWithinPatch(hFig,inDragMode,hAx,scrollPatch,cx,isOverBar)
            else:
                # Perform cleanup
                mouseOutsidePatch(hFig,inDragMode,hAx)
        # Try to chain the original WindowButtonMotionFcn (if available)
        try:
            hgfeval(getappdata(hFig,'scrollplot_oldButtonMotionFcn'))
        finally:
            pass
    finally:
        pass
    
    rmappdataIfExists(hFig,'scrollBar_inProgress')
    
    try:
        warning(oldWarn)
    finally:
        pass
    
    #end  # mouseMoveCallback  ##ok for Matlab 6 compatibility
    
    ## Mouse click down callback function
    
@function
def mouseDownCallback(varargin=None,*args,**kwargs):
    varargin = mouseDownCallback.varargin
    nargin = mouseDownCallback.nargin

    try:
        # Modify the cursor shape (close hand)
        hFig=copy(gcbf)
# scrollplot.m:976
        if logical_and(isempty(hFig),logical_not(isempty(varargin))):
            hFig=ancestor(varargin[1],'figure')
# scrollplot.m:978
        if logical_or(isempty(hFig),logical_not(ishandle(hFig))):
            return
        setappdata(hFig,'scrollplot_mouseUpPointer',getptr(hFig))
        newPtr=getappdata(hFig,'scrollplot_mouseDownPointer')
# scrollplot.m:982
        if logical_not(isempty(newPtr)):
            setptr(hFig,newPtr)
        # Determine the clicked object: patch, left bar or right bar
        hAx=get(hFig,'currentAxes')
# scrollplot.m:988
        if isempty(hAx):
            return
        axName=get(hAx,'userdata')
# scrollplot.m:990
        limits=get(hAx,concat([axName,'Lim']))
# scrollplot.m:991
        cp=get(hAx,'CurrentPoint')
# scrollplot.m:992
        barXs=concat([- inf,inf])
# scrollplot.m:995
        scrollBarIdx=[]
# scrollplot.m:996
        scrollPatch=findobj(hAx,'tag','scrollPatch')
# scrollplot.m:997
        if logical_not(isempty(scrollPatch)):
            scrollPatch=scrollPatch(1)
# scrollplot.m:999
            dataStr=concat([axName,'Data'])
# scrollplot.m:1000
            barXs=unique(get(scrollPatch,dataStr))
# scrollplot.m:1001
            if isempty(barXs):
                return
            if strcmpi(axName,'x'):
                cx=cp(1,1)
# scrollplot.m:1004
            else:
                cx=cp(1,2)
# scrollplot.m:1006
            if strcmpi(get(hAx,concat([axName,'Scale'])),'log'):
                fuzz=dot(0.01,diff(log(abs(limits))))
# scrollplot.m:1009
                barXs=log10(barXs)
# scrollplot.m:1010
                cx=log10(cx)
# scrollplot.m:1011
            else:
                fuzz=dot(0.01,diff(limits))
# scrollplot.m:1013
            inTest=abs(cx - barXs) < fuzz
# scrollplot.m:1015
            scrollBarIdx=find(inTest)
# scrollplot.m:1016
            scrollBarIdx=scrollBarIdx(min(arange(1,end())))
# scrollplot.m:1017
            if strcmpi(get(hAx,concat([axName,'Scale'])),'log'):
                cx=10 ** cx
# scrollplot.m:1019
                barXs=10.0 ** barXs
# scrollplot.m:1020
            # Re-sort side bars (might have been dragged one over the other...)
            scrollBars=sort(findobj(hAx,'tag','scrollBar'))
# scrollplot.m:1024
            barsXs=getFirstVals(get(scrollBars,dataStr))
# scrollplot.m:1026
            if barsXs(1) > barsXs(2):
                set(scrollBars(1),dataStr,dot(barsXs(2),concat([1,1])))
                set(scrollBars(2),dataStr,dot(barsXs(1),concat([1,1])))
        setappdata(hFig,'scrollplot_clickedBarIdx',scrollBarIdx)
        setappdata(hFig,'scrollplot_originalX',cx)
        setappdata(hFig,'scrollplot_originalLimits',barXs)
    finally:
        pass
    
    #end  # mouseDownCallback  ##ok for Matlab 6 compatibility
    
    ## Mouse click up callback function
    
@function
def mouseUpCallback(varargin=None,*args,**kwargs):
    varargin = mouseUpCallback.varargin
    nargin = mouseUpCallback.nargin

    try:
        # Restore the previous (pre-click) cursor shape
        hFig=copy(gcbf)
# scrollplot.m:1045
        if logical_and(isempty(hFig),logical_not(isempty(varargin))):
            hFig=varargin[3]
# scrollplot.m:1047
            if isempty(hFig):
                hFig=ancestor(varargin[1],'figure')
# scrollplot.m:1049
        if logical_or(isempty(hFig),logical_not(ishandle(hFig))):
            return
        if isappdata(hFig,'scrollplot_mouseUpPointer'):
            mouseUpPointer=getappdata(hFig,'scrollplot_mouseUpPointer')
# scrollplot.m:1054
            set(hFig,mouseUpPointer[arange()])
            rmappdata(hFig,'scrollplot_mouseUpPointer')
        # Cleanup data no longer needed
        rmappdataIfExists(hFig,'scrollplot_clickedBarIdx')
        rmappdataIfExists(hFig,'scrollplot_originalX')
        rmappdataIfExists(hFig,'scrollplot_originalLimits')
        oldFcn=getappdata(hFig,'scrollplot_oldButtonUpFcn')
# scrollplot.m:1065
        if logical_and(logical_and(logical_not(isempty(oldFcn)),logical_not(isequal(oldFcn,mouseUpCallback))),(logical_or(logical_not(iscell(oldFcn)),logical_not(isequal(oldFcn[1],mouseUpCallback))))):
            try:
                hgfeval(oldFcn)
            finally:
                pass
    finally:
        pass
    
    #end  # mouseUpCallback  ##ok for Matlab 6 compatibility
    
    ## Remove appdata if available
    
@function
def rmappdataIfExists(handle=None,name=None,*args,**kwargs):
    varargin = rmappdataIfExists.varargin
    nargin = rmappdataIfExists.nargin

    if isappdata(handle,name):
        rmappdata(handle,name)
    
    #end  # rmappdataIfExists  ##ok for Matlab 6 compatibility
    
    ## Get the figure's java axis component
    
@function
def getAxisComponent(hFig=None,*args,**kwargs):
    varargin = getAxisComponent.varargin
    nargin = getAxisComponent.nargin

    try:
        if isappdata(hFig,'scrollplot_axisComponent'):
            axisComponent=getappdata(hFig,'scrollplot_axisComponent')
# scrollplot.m:1090
        else:
            axisComponent=[]
# scrollplot.m:1092
            try:
                oldWarn=warning('off','MATLAB:HandleGraphics:ObsoletedProperty:JavaFrame')
# scrollplot.m:1093
            finally:
                pass
            javaFrame=get(hFig,'JavaFrame')
# scrollplot.m:1094
            axisComponent=get(javaFrame,'AxisComponent')
# scrollplot.m:1095
            axisComponent=handle(axisComponent,'CallbackProperties')
# scrollplot.m:1096
            if logical_not(isprop(axisComponent,'MouseReleasedCallback')):
                axisComponent=[]
# scrollplot.m:1098
            else:
                setappdata(hFig,'scrollplot_axisComponent',axisComponent)
    finally:
        pass
    
    try:
        warning(oldWarn)
    finally:
        pass
    
    #end  # getAxisComponent  ##ok for Matlab 6 compatibility
    
    ## Get the scroll axes that the mouse is currently over
    
@function
def getCurrentScrollAx(hFig=None,*args,**kwargs):
    varargin = getCurrentScrollAx.varargin
    nargin = getCurrentScrollAx.nargin

    try:
        hAx=[]
# scrollplot.m:1112
        scrollAxes=findall(hFig,'tag','scrollAx')
# scrollplot.m:1113
        if isempty(scrollAxes):
            return hAx
        for axIdx in arange(1,length(scrollAxes)).reshape(-1):
            scrollPos[axIdx,arange()]=getPixelPos(scrollAxes(axIdx))
# scrollplot.m:1116
        cp=get(hFig,'CurrentPoint')
# scrollplot.m:1118
        inXTest=logical_and((scrollPos(arange(),1) <= cp(1)),(cp(1) <= scrollPos(arange(),1) + scrollPos(arange(),3)))
# scrollplot.m:1119
        inYTest=logical_and((scrollPos(arange(),2) <= cp(2)),(cp(2) <= scrollPos(arange(),2) + scrollPos(arange(),4)))
# scrollplot.m:1120
        hAx=scrollAxes(logical_and(inXTest,inYTest))
# scrollplot.m:1121
        hAx=hAx(min(arange(1,end())))
# scrollplot.m:1122
    finally:
        pass
    
    #end  # getCurrentScrollAx  ##ok for Matlab 6 compatibility
    
    ## Get pixel position of an HG object
    
@function
def getPixelPos(hObj=None,*args,**kwargs):
    varargin = getPixelPos.varargin
    nargin = getPixelPos.nargin

    try:
        # getpixelposition is unvectorized unfortunately!
        pos=getpixelposition(hObj)
# scrollplot.m:1133
    finally:
        pass
    
    #end  # getPixelPos  ##ok for Matlab 6 compatibility
    
    ## Get position of an HG object in specified units
    
@function
def getPos(hObj=None,units=None,*args,**kwargs):
    varargin = getPos.varargin
    nargin = getPos.nargin

    # Matlab 6 did not have hgconvertunits so use the old way...
    oldUnits=get(hObj,'units')
# scrollplot.m:1143
    if strcmpi(oldUnits,units):
        pos=get(hObj,'pos')
# scrollplot.m:1145
    else:
        set(hObj,'units',units)
        pos=get(hObj,'pos')
# scrollplot.m:1148
        set(hObj,'units',oldUnits)
    
    #end  # getPos  ##ok for Matlab 6 compatibility
    
    ## Temporary setting property value for a read-only property
    
@function
def setOnce(hndl=None,propName=None,propValue=None,*args,**kwargs):
    varargin = setOnce.varargin
    nargin = setOnce.nargin

    try:
        try:
            prop=findprop(hndl,propName)
# scrollplot.m:1157
            oldSetState=get(prop,'AccessFlags.PublicSet')
# scrollplot.m:1158
            set(prop,'AccessFlags.PublicSet','on')
            set(hndl,propName,propValue)
            set(prop,'AccessFlags.PublicSet',oldSetState)
        finally:
            pass
    finally:
        pass
    
    #end  # setOnce  ##ok for Matlab 6 compatibility
    
    ## Callback for parent axes property changes
    
@function
def parentAxesChanged(schemaProp=None,eventData=None,hFig=None,hAx=None,hScrollPatch=None,hScrollBars=None,propName=None,*args,**kwargs):
    varargin = parentAxesChanged.varargin
    nargin = parentAxesChanged.nargin

    try:
        if logical_or(isempty(hFig),logical_not(ishandle(hFig))):
            return
        newPropVal=get(hAx,propName)
# scrollplot.m:1177
        hScroll=get(hScrollPatch,'Parent')
# scrollplot.m:1178
        axName=get(hScroll,'userdata')
# scrollplot.m:1179
        if isappdata(hFig,'scrollBar_inProgress'):
            # Update the special prop values
            if strcmpi(propName,concat([axName,'Lim'])):
                setOnce(handle(hScroll),'ScrollMin',newPropVal(1))
                setOnce(handle(hScroll),'ScrollMax',newPropVal(2))
            return
        if 'XLim' == propName:
            if strcmpi(axName,'x'):
                set(hScrollPatch,'XData',newPropVal(concat([1,1,2,2])))
                set(hScrollBars(1),'Xdata',newPropVal(concat([1,1])))
                set(hScrollBars(2),'Xdata',newPropVal(concat([2,2])))
                setOnce(handle(hScroll),'ScrollMin',newPropVal(1))
                setOnce(handle(hScroll),'ScrollMax',newPropVal(2))
        else:
            if 'YLim' == propName:
                if strcmpi(axName,'y'):
                    set(hScrollPatch,'YData',newPropVal(concat([1,2,2,1])))
                    set(hScrollBars(1),'Ydata',newPropVal(concat([1,1])))
                    set(hScrollBars(2),'Ydata',newPropVal(concat([2,2])))
                    setOnce(handle(hScroll),'ScrollMin',newPropVal(1))
                    setOnce(handle(hScroll),'ScrollMax',newPropVal(2))
            else:
                if 'Position' == propName:
                    if strcmpi(axName,'x'):
                        newScrollPos=multiply(newPropVal,concat([1,1,1,0.1 / 0.8]))
# scrollplot.m:1209
                        newScrollPos=newScrollPos - concat([0,dot(0.2 / 0.8,newPropVal(4)),0,0])
# scrollplot.m:1210
                    else:
                        newScrollPos=multiply(newPropVal,concat([1,1,0.1 / 0.8,1]))
# scrollplot.m:1212
                        newScrollPos=newScrollPos + concat([dot((1 + 0.05 / 0.8),newPropVal(3)),0,0,0])
# scrollplot.m:1213
                    axUnits=get(hAx,'Units')
# scrollplot.m:1215
                    set(hScroll,'Units',axUnits,'Position',newScrollPos)
                else:
                    if cellarray(['Units','Parent','XDir','YDir','XScale','YScale']) == propName:
                        set(hScroll,propName,newPropVal)
                    else:
                        # Do nothing...
                        pass
    finally:
        pass
    
    #end  # parentAxesChanged  ##ok for Matlab 6 compatibility
    
    ## Determine whether a current mode manager should be active or not (filtered)
    
@function
def shouldModeBeInactiveFcn(hObj=None,eventData=None,*args,**kwargs):
    varargin = shouldModeBeInactiveFcn.varargin
    nargin = shouldModeBeInactiveFcn.nargin

    try:
        shouldModeBeInactive=0
# scrollplot.m:1233
        hFig=ancestor(hObj,'figure')
# scrollplot.m:1234
        hScrollAx=getCurrentScrollAx(hFig)
# scrollplot.m:1235
        shouldModeBeInactive=logical_not(isempty(hScrollAx))
# scrollplot.m:1236
    finally:
        pass
    
    #end  # shouldModeBeActiveFcn  ##ok for Matlab 6 compatibility
    
    ## hgfeval replacement for Matlab 6 compatibility
    
@function
def hgfeval(fcn=None,varargin=None,*args,**kwargs):
    varargin = hgfeval.varargin
    nargin = hgfeval.nargin

    if isempty(fcn):
        return
    
    if iscell(fcn):
        feval(fcn[1],varargin[arange()],fcn[arange(2,end())])
    else:
        if ischar(fcn):
            evalin('base',fcn)
        else:
            feval(fcn,varargin[arange()])
    
    #end  # hgfeval  ##ok for Matlab 6 compatibility
    
    ## Axis to screen coordinate transformation
    
@function
def axis2Screen(ax=None,*args,**kwargs):
    varargin = axis2Screen.varargin
    nargin = axis2Screen.nargin

    #   computes a coordinate transformation T = [xo,yo,rx,ry] that
#   relates the normalized axes coordinates [xa,ya] of point [xo,yo]
#   to its screen coordinate [xs,ys] (in the root units) by:
#       xs = xo + rx * xa
#       ys = yo + ry * ya
    
    #   See also SISOTOOL
    
    #   Note: this is a modified internal function within moveptr()
    
    # Get axes normalized position in figure
    T=getPos(ax,'normalized')
# scrollplot.m:1268
    
    # Note: this fixes a bug in Matlab 7's moveptr implementation
    parent=get(ax,'Parent')
# scrollplot.m:1272
    while logical_not(isempty(parent)):

        # Transform norm. axis coord -> parent coord.
        if isequal(parent,0):
            parentPos=get(0,'ScreenSize')
# scrollplot.m:1276
        else:
            parentPos=getPos(parent,'normalized')
# scrollplot.m:1278
        T[arange(1,2)]=parentPos(arange(1,2)) + multiply(parentPos(arange(3,4)),T(arange(1,2)))
# scrollplot.m:1280
        T[arange(3,4)]=multiply(parentPos(arange(3,4)),T(arange(3,4)))
# scrollplot.m:1281
        parent=get(parent,'Parent')
# scrollplot.m:1282

    
    #end  # axis2Screen  ##ok for Matlab 6 compatibility
    
    ## Get centran axis location
    
@function
def getCenterCoord(hAx=None,axName=None,*args,**kwargs):
    varargin = getCenterCoord.varargin
    nargin = getCenterCoord.nargin

    limits=get(hAx,concat([axName,'Lim']))
# scrollplot.m:1288
    if strcmpi(get(hAx,concat([axName,'Scale'])),'log'):
        axisCoord=sqrt(abs(prod(limits)))
# scrollplot.m:1290
    else:
        axisCoord=mean(limits)
# scrollplot.m:1292
    
    #end  #getCenterCoord  ##ok for Matlab 6 compatibility
    
    ## Get normalized axis coordinates
    
@function
def getNormCoord(hAx=None,axName=None,curPos=None,*args,**kwargs):
    varargin = getNormCoord.varargin
    nargin = getNormCoord.nargin

    limits=get(hAx,concat([axName,'Lim']))
# scrollplot.m:1298
    if strcmpi(get(hAx,concat([axName,'Scale'])),'log'):
        normCoord=(log2(curPos) - log2(limits(1))) / diff(log2(limits))
# scrollplot.m:1300
    else:
        normCoord=(curPos - limits(1)) / diff(limits)
# scrollplot.m:1302
    
    #end  # getNormCoord ##ok for Matlab 6 compatibility
    
    ## moveptr replacement for Matlab 6 compatibility
    
@function
def moveptr(hAx=None,x=None,y=None,*args,**kwargs):
    varargin = moveptr.varargin
    nargin = moveptr.nargin

    # Compute normalized axis coordinates
    NormX=getNormCoord(hAx,'x',x)
# scrollplot.m:1309
    NormY=getNormCoord(hAx,'y',y)
# scrollplot.m:1310
    
    Transform=axis2Screen(hAx)
# scrollplot.m:1313
    NewLoc=Transform(arange(1,2)) + multiply(Transform(arange(3,4)),concat([NormX,NormY]))
# scrollplot.m:1314
    
    set(0,'PointerLocation',NewLoc)
    #end  # moveptr  ##ok for Matlab 6 compatibility
    
    ## UiContextMenu callback - Move cursor to center of requested element
    
@function
def moveCursor(varargin=None,*args,**kwargs):
    varargin = moveCursor.varargin
    nargin = moveCursor.nargin

    try:
        # Get the x,y location of the center of the requested object
        hScroll=handle(gca)
# scrollplot.m:1324
        hObj=get(gcbo,'UserData')
# scrollplot.m:1325
        x=mean(get(hObj,'XData'))
# scrollplot.m:1326
        y=mean(get(hObj,'YData'))
# scrollplot.m:1327
        # Note: Matlab 6 did not have moveptr() so we use a local version above
        #moveptr(hScroll, 'init');
        #moveptr(hScroll, 'move', x, y);
        moveptr(hScroll,x,y)
        mouseMoveCallback
        drawnow
    finally:
        pass
    
    #end  # moveCursor  ##ok for Matlab 6 compatibility
    
    ## Callback when scroll axes are deleted
    
@function
def deleteScrollAx(varargin=None,*args,**kwargs):
    varargin = deleteScrollAx.varargin
    nargin = deleteScrollAx.nargin

    try:
        # Update the parent Axes position
        hScroll=varargin[1]
# scrollplot.m:1348
        updateParentPos([],[],hScroll,'off')
    finally:
        pass
    
    #end  # deleteScrollAx  ##ok for Matlab 6 compatibility
    
    ## Update parent figure position based on scroll axes visibility
    
@function
def updateParentPos(schemaProp=None,eventData=None,hScroll=None,scrollVisibility=None,*args,**kwargs):
    varargin = updateParentPos.varargin
    nargin = updateParentPos.nargin

    try:
        if nargin < 4:
            scrollVisibility=get(hScroll,'visible')
# scrollplot.m:1360
        # Update the parent Axes position
        hAx=get(hScroll,'ParentAxesHandle')
# scrollplot.m:1364
        axPos=get(hAx,'position')
# scrollplot.m:1365
        axName=get(hScroll,'userdata')
# scrollplot.m:1366
        hLabel=get(hAx,concat([axName,'Label']))
# scrollplot.m:1367
        set(hLabel,'units','normalized')
        oldPos=get(hLabel,'position')
# scrollplot.m:1369
        if strcmpi(scrollVisibility,'off'):
            ax_dy1=1 / 0.8
# scrollplot.m:1372
            ax_dy2=- 1 / 0.8
# scrollplot.m:1373
            label_delta=0.2 / 0.8
# scrollplot.m:1374
        else:
            ax_dy1=0.8
# scrollplot.m:1376
            ax_dy2=1
# scrollplot.m:1377
            label_delta=- 0.2 / 0.8
# scrollplot.m:1378
        if strcmpi(axName,'x'):
            newPlotPos=multiply(axPos,concat([1,1,1,ax_dy1])) + concat([0,dot(dot(0.2,axPos(4)),ax_dy2),0,0])
# scrollplot.m:1382
        else:
            newPlotPos=multiply(axPos,concat([1,1,ax_dy1,1]))
# scrollplot.m:1384
        set(hAx,'Position',newPlotPos)
        if strcmpi(axName,'x'):
            if logical_and(logical_not(isempty(oldPos)),oldPos(2)) < 0:
                # Only fix if the X label is on the bottom (usually yes)
                set(hLabel,'position',oldPos + concat([0,label_delta,0]))
        else:
            if logical_and(logical_not(isempty(oldPos)),oldPos(1)) > 0:
                # Only fix if the Y label is on the right side (usually not)
                set(hLabel,'position',oldPos - concat([label_delta,0,0]))
        # Show/hide all the axes children (scroll patch, side-bars, text)
        set(findall(hScroll),'Visible',scrollVisibility)
        hFig=ancestor(hScroll,'figure')
# scrollplot.m:1405
        rmappdata(hFig,'scrollplot_axisComponent')
    finally:
        pass
    
    #end  # updateParentPos  ##ok for Matlab 6 compatibility
    
    ## Set mouse pointer
# this is a copy of setptr.m, copied here to remove reliance on this unsupported external function
    
@function
def setptr(fig=None,curs=None,fname=None,*args,**kwargs):
    varargin = setptr.varargin
    nargin = setptr.nargin

    #SETPTR Set figure pointer.
#   SETPTR(FIG,CURSOR_NAME) sets the cursor of the figure w/ handle FIG 
#   according to the cursor_name:
#      'hand'    - open hand for panning indication
#      'hand1'   - open hand with a 1 on the back
#      'hand2'   - open hand with a 2 on the back
#      'closedhand' - closed hand for panning while mouse is down
#      'glass'   - magnifying glass
#      'glassplus' - magnifying glass with '+' in middle
#      'glassminus' - magnifying glass with '-' in middle
#      'lrdrag'  - left/right drag cursor
#      'ldrag'   - left drag cursor
#      'rdrag'   - right drag cursor
#      'uddrag'  - up/down drag cursor
#      'udrag'   - up drag cursor
#      'ddrag'   - down drag cursor
#      'add'     - arrow with + sign
#      'addzero' - arrow with 'o'
#      'addpole' - arrow with 'x'
#      'eraser'  - eraser
#      'help'    - arrow with question mark ?
#      'modifiedfleur' - modified fleur
#      'datacursor' - modified fleur with a hole in the center
#      'rotate' - modified fleur
#      [ crosshair | fullcrosshair | {arrow} | ibeam | watch | topl | topr ...
#      | botl | botr | left | top | right | bottom | circle | cross | fleur ]
#           - standard figure cursors
    
    #   SetData=setptr(CURSOR_NAME) returns a cell array containing 
#   the Property Value pairs which correctly set the pointer to 
#   the CURSOR_NAME specified. 
#   
#   Example:
#       f = figure;
#       SetData=setptr('hand');set(f,SetData{:})
    
    #   See also GETPTR
    
    #   Author: T. Krauss, 10/95
#   Copyright 1984-2012 The MathWorks, Inc.
    
    # now for custom cursors:
    stringflag=0
# scrollplot.m:1457
    if ischar(fig):
        if nargin == 2:
            fname=copy(curs)
# scrollplot.m:1459
        curs=copy(fig)
# scrollplot.m:1460
        fig=[]
# scrollplot.m:1460
        stringflag=1
# scrollplot.m:1461
    
    mac_curs=1
# scrollplot.m:1464
    if 'hand' == curs:
        cdata=concat([NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,1,NaN,1,2,2,1,1,1,NaN,NaN,NaN,NaN,NaN,NaN,1,2,2,1,1,2,2,1,2,2,1,NaN,NaN,NaN,NaN,NaN,1,2,2,1,1,2,2,1,2,2,1,NaN,1,NaN,NaN,NaN,NaN,1,2,2,1,2,2,1,2,2,1,1,2,1,NaN,NaN,NaN,1,2,2,1,2,2,1,2,2,1,2,2,1,NaN,1,1,NaN,1,2,2,2,2,2,2,2,1,2,2,1,1,2,2,1,1,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,1,2,2,2,2,2,2,2,2,2,1,NaN,NaN,1,2,2,2,2,2,2,2,2,2,2,2,2,1,NaN,NaN,NaN,1,2,2,2,2,2,2,2,2,2,2,2,1,NaN,NaN,NaN,1,2,2,2,2,2,2,2,2,2,2,1,NaN,NaN,NaN,NaN,NaN,1,2,2,2,2,2,2,2,2,2,1,NaN,NaN,NaN,NaN,NaN,NaN,1,2,2,2,2,2,2,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,2,2,2,2,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,2,2,2,2,2,1,NaN,NaN,NaN])
# scrollplot.m:1467
        hotspot=concat([10,9])
# scrollplot.m:1485
        mac_curs=0
# scrollplot.m:1486
    else:
        if 'closedhand' == curs:
            cdata=concat([NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,1,NaN,1,1,NaN,1,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,2,1,2,2,1,2,2,1,1,NaN,NaN,NaN,NaN,NaN,1,2,2,2,2,2,2,2,2,1,2,1,NaN,NaN,NaN,NaN,NaN,1,2,2,2,2,2,2,2,2,2,1,NaN,NaN,NaN,NaN,1,1,2,2,2,2,2,2,2,2,2,1,NaN,NaN,NaN,1,2,2,2,2,2,2,2,2,2,2,2,1,NaN,NaN,NaN,1,2,2,2,2,2,2,2,2,2,2,2,1,NaN,NaN,NaN,1,2,2,2,2,2,2,2,2,2,2,1,NaN,NaN,NaN,NaN,NaN,1,2,2,2,2,2,2,2,2,2,1,NaN,NaN,NaN,NaN,NaN,NaN,1,2,2,2,2,2,2,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,2,2,2,2,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,2,2,2,2,2,1,NaN,NaN,NaN])
# scrollplot.m:1488
            hotspot=concat([10,9])
# scrollplot.m:1506
            mac_curs=0
# scrollplot.m:1507
        else:
            if 'hand1' == curs:
                d=concat(['01801A702648264A124D1249680998818982408220822084108409C804080408','01801BF03FF83FFA1FFF1FFF6FFFFFFFFFFE7FFE3FFE3FFC1FFC0FF807F807F8','00090008']).T
# scrollplot.m:1509
            else:
                if 'hand2' == curs:
                    d=concat(['01801A702648264A124D1249680998C18922402220422084110409E804080408','01801BF03FF83FFA1FFF1FFF6FFFFFFFFFFE7FFE3FFE3FFC1FFC0FF807F807F8','00090008']).T
# scrollplot.m:1513
                else:
                    if 'glass' == curs:
                        d=concat(['0F0030C04020402080108010801080104020402030F00F38001C000E00070002','0F0035C06AA05560AAB0D550AAB0D5506AA055703AF80F7C003E001F000F0007','00060006']).T
# scrollplot.m:1517
                    else:
                        if 'glassplus' == curs:
                            o=copy(NaN)
# scrollplot.m:1521
                            w=2
# scrollplot.m:1521
                            k=1
# scrollplot.m:1521
                            cdata=concat([o,o,o,o,k,k,k,k,o,o,o,o,o,o,o,o,o,o,k,k,o,w,o,w,k,k,o,o,o,o,o,o,o,k,w,o,w,k,k,o,w,o,k,o,o,o,o,o,o,k,o,w,o,k,k,w,o,w,k,o,o,o,o,o,k,o,w,o,w,k,k,o,w,o,w,k,o,o,o,o,k,w,k,k,k,k,k,k,k,k,o,k,o,o,o,o,k,o,k,k,k,k,k,k,k,k,w,k,o,o,o,o,k,w,o,w,o,k,k,w,o,w,o,k,o,o,o,o,o,k,w,o,w,k,k,o,w,o,k,o,o,o,o,o,o,k,o,w,o,k,k,w,o,w,k,w,o,o,o,o,o,o,k,k,w,o,w,o,k,k,k,k,w,o,o,o,o,o,o,o,k,k,k,k,o,w,k,k,k,w,o,o,o,o,o,o,o,o,o,o,o,o,w,k,k,k,w,o,o,o,o,o,o,o,o,o,o,o,o,w,k,k,k,w,o,o,o,o,o,o,o,o,o,o,o,o,w,k,k,k,o,o,o,o,o,o,o,o,o,o,o,o,o,w,k,w])
# scrollplot.m:1522
                            hotspot=concat([6,6])
# scrollplot.m:1540
                            mac_curs=0
# scrollplot.m:1541
                        else:
                            if 'glassminus' == curs:
                                o=copy(NaN)
# scrollplot.m:1543
                                w=2
# scrollplot.m:1543
                                k=1
# scrollplot.m:1543
                                cdata=concat([o,o,o,o,k,k,k,k,o,o,o,o,o,o,o,o,o,o,k,k,o,w,o,w,k,k,o,o,o,o,o,o,o,k,w,o,w,o,w,o,w,o,k,o,o,o,o,o,o,k,o,w,o,w,o,w,o,w,k,o,o,o,o,o,k,o,w,o,w,o,w,o,w,o,w,k,o,o,o,o,k,w,k,k,k,k,k,k,k,k,o,k,o,o,o,o,k,o,k,k,k,k,k,k,k,k,w,k,o,o,o,o,k,w,o,w,o,w,o,w,o,w,o,k,o,o,o,o,o,k,w,o,w,o,w,o,w,o,k,o,o,o,o,o,o,k,o,w,o,w,o,w,o,w,k,w,o,o,o,o,o,o,k,k,w,o,w,o,k,k,k,k,w,o,o,o,o,o,o,o,k,k,k,k,o,w,k,k,k,w,o,o,o,o,o,o,o,o,o,o,o,o,w,k,k,k,w,o,o,o,o,o,o,o,o,o,o,o,o,w,k,k,k,w,o,o,o,o,o,o,o,o,o,o,o,o,w,k,k,k,o,o,o,o,o,o,o,o,o,o,o,o,o,w,k,w])
# scrollplot.m:1544
                                hotspot=concat([6,6])
# scrollplot.m:1562
                                mac_curs=0
# scrollplot.m:1563
                            else:
                                if 'lrdrag' == curs:
                                    d=concat(['00000280028002800AA01AB03EF87EFC3EF81AB00AA002800280028000000000','07C007C007C00FE01FF03FF87FFCFFFE7FFC3FF81FF00FE007C007C007C00000','00070007']).T
# scrollplot.m:1565
                                else:
                                    if 'ldrag' == curs:
                                        d=concat(['00000200020002000A001A003E007E003E001A000A0002000200020000000000','0700070007000F001F003F007F00FF007F003F001F000F000700070007000000','00070007']).T
# scrollplot.m:1569
                                    else:
                                        if 'rdrag' == curs:
                                            d=concat(['000000800080008000A000B000F800FC00F800B000A000800080008000000000','00C000C000C000E000F000F800FC00FE00FC00F800F000E000C000C000C00000','00070007']).T
# scrollplot.m:1573
                                        else:
                                            if 'uddrag' == curs:
                                                d=concat(['000000000100038007C00FE003807FFC00007FFC03800FE007C0038001000000','00000100038007C00FE01FF0FFFEFFFEFFFEFFFEFFFE1FF00FE007C003800100','00080007']).T
# scrollplot.m:1577
                                            else:
                                                if 'udrag' == curs:
                                                    d=concat(['000000000100038007C00FE003807FFC00000000000000000000000000000000','00000100038007C00FE01FF0FFFEFFFEFFFE0000000000000000000000000000','00080007']).T
# scrollplot.m:1581
                                                else:
                                                    if 'ddrag' == curs:
                                                        d=concat(['0000000000000000000000000000000000007FFC03800FE007C0038001000000','00000000000000000000000000000000FFFEFFFEFFFE1FF00FE007C003800100','00080007']).T
# scrollplot.m:1585
                                                    else:
                                                        if 'add' == curs:
                                                            cdata=concat([2,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,NaN,NaN,NaN,NaN,NaN,2,1,2,NaN,NaN,NaN,NaN,NaN,NaN,2,1,2,NaN,NaN,NaN,NaN,2,1,1,2,NaN,NaN,NaN,NaN,2,2,1,2,2,NaN,NaN,NaN,2,1,1,1,2,NaN,NaN,2,1,1,1,1,1,2,NaN,NaN,2,1,1,1,1,2,NaN,NaN,2,2,1,2,2,NaN,NaN,NaN,2,1,1,1,1,1,2,NaN,NaN,2,1,2,NaN,NaN,NaN,NaN,2,1,1,1,1,1,1,2,NaN,NaN,2,NaN,NaN,NaN,NaN,NaN,2,1,1,1,1,1,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,1,1,1,1,1,1,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,2,1,1,1,1,1,2,2,2,2,2,NaN,NaN,NaN,NaN,NaN,2,1,1,2,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,1,2,NaN,2,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,2,NaN,NaN,2,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,NaN,NaN,NaN,NaN,2,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,2,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN])
# scrollplot.m:1589
                                                            hotspot=concat([1,1])
# scrollplot.m:1607
                                                            mac_curs=0
# scrollplot.m:1608
                                                        else:
                                                            if 'addpole' == curs:
                                                                cdata=concat([2,2,NaN,NaN,NaN,NaN,NaN,2,2,2,NaN,NaN,2,2,NaN,NaN,2,1,2,NaN,NaN,NaN,NaN,2,1,2,NaN,2,1,2,NaN,NaN,2,1,1,2,NaN,NaN,NaN,NaN,2,1,2,1,2,2,NaN,NaN,2,1,1,1,2,NaN,NaN,NaN,NaN,2,1,2,NaN,NaN,NaN,NaN,2,1,1,1,1,2,NaN,NaN,2,1,2,1,2,2,NaN,NaN,2,1,1,1,1,1,2,2,1,2,NaN,2,1,2,NaN,NaN,2,1,1,1,1,1,1,2,2,NaN,NaN,NaN,2,2,NaN,NaN,2,1,1,1,1,1,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,1,1,1,1,1,1,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,2,1,1,1,1,1,2,2,2,2,2,NaN,NaN,NaN,NaN,NaN,2,1,1,2,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,1,2,NaN,2,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,2,NaN,NaN,2,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,NaN,NaN,NaN,NaN,2,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,2,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN])
# scrollplot.m:1610
                                                                hotspot=concat([1,1])
# scrollplot.m:1628
                                                                mac_curs=0
# scrollplot.m:1629
                                                            else:
                                                                if 'addzero' == curs:
                                                                    cdata=concat([2,2,NaN,NaN,NaN,NaN,NaN,NaN,2,2,2,2,2,NaN,NaN,NaN,2,1,2,NaN,NaN,NaN,NaN,2,2,1,1,1,2,2,NaN,NaN,2,1,1,2,NaN,NaN,NaN,2,1,2,2,2,1,2,NaN,NaN,2,1,1,1,2,NaN,NaN,2,1,2,NaN,2,1,2,NaN,NaN,2,1,1,1,1,2,NaN,2,1,2,2,2,1,2,NaN,NaN,2,1,1,1,1,1,2,2,2,1,1,1,2,2,NaN,NaN,2,1,1,1,1,1,1,2,2,2,2,2,2,NaN,NaN,NaN,2,1,1,1,1,1,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,1,1,1,1,1,1,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,2,1,1,1,1,1,2,2,2,2,2,NaN,NaN,NaN,NaN,NaN,2,1,1,2,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,1,2,NaN,2,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,2,NaN,NaN,2,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,NaN,NaN,NaN,NaN,2,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,1,1,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,2,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN])
# scrollplot.m:1631
                                                                    hotspot=concat([1,1])
# scrollplot.m:1649
                                                                    mac_curs=0
# scrollplot.m:1650
                                                                else:
                                                                    if 'eraser' == curs:
                                                                        cdata=concat([NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,1,1,1,1,1,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,1,2,2,2,2,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,2,2,2,2,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,2,1,2,2,2,2,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,2,1,2,2,2,2,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,2,1,2,2,2,2,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,2,1,2,2,2,2,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,2,1,2,2,2,2,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,2,1,2,2,2,2,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,2,1,1,1,1,1,1,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,2,2,2,2,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,1,1,1,1,1,1,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN])
# scrollplot.m:1652
                                                                        hotspot=concat([2,1])
# scrollplot.m:1670
                                                                        mac_curs=0
# scrollplot.m:1671
                                                                    else:
                                                                        if 'modifiedfleur' == curs:
                                                                            cdata=concat([NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,1,1,1,1,1,2,1,1,1,1,1,1,1,NaN,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,NaN,1,1,1,1,1,1,2,1,1,1,1,1,1,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN])
# scrollplot.m:1673
                                                                            hotspot=concat([8,8])
# scrollplot.m:1691
                                                                            mac_curs=0
# scrollplot.m:1692
                                                                        else:
                                                                            if 'datacursor' == curs:
                                                                                cdata=concat([NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,1,1,1,1,NaN,NaN,NaN,1,1,1,1,1,1,NaN,1,2,2,2,2,2,NaN,NaN,NaN,2,2,2,2,2,2,1,NaN,1,1,1,1,1,NaN,NaN,NaN,1,1,1,1,1,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,2,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN])
# scrollplot.m:1694
                                                                                hotspot=concat([8,8])
# scrollplot.m:1712
                                                                                mac_curs=0
# scrollplot.m:1713
                                                                            else:
                                                                                if 'rotate' == curs:
                                                                                    cdata=concat([NaN,NaN,NaN,NaN,NaN,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,1,2,1,1,1,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,1,1,1,2,2,2,2,1,1,NaN,NaN,NaN,NaN,NaN,2,1,1,1,1,2,NaN,NaN,NaN,2,2,1,NaN,NaN,NaN,NaN,2,2,2,2,2,NaN,NaN,NaN,NaN,NaN,NaN,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,NaN,NaN,NaN,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,NaN,NaN,NaN,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,NaN,NaN,NaN,NaN,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,NaN,NaN,NaN,NaN,NaN,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,1,NaN,NaN,NaN,NaN,NaN,1,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,NaN,NaN,1,NaN,NaN,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,2,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN])
# scrollplot.m:1715
                                                                                    hotspot=concat([8,8])
# scrollplot.m:1733
                                                                                    mac_curs=0
# scrollplot.m:1734
                                                                                else:
                                                                                    if 'help' == curs:
                                                                                        d=concat(['000040006000707C78FE7CC67EC67F0C7F987C306C3046000630033003000000','C000E000F07CF8FEFDFFFFFFFFEFFFDEFFFCFFF8FE78EF78CF7887F807F80380','00010001']).T
# scrollplot.m:1736
                                                                                    else:
                                                                                        if 'file' == curs:
                                                                                            f=fopen(fname)
# scrollplot.m:1740
                                                                                            d=fread(f)
# scrollplot.m:1741
                                                                                            if length(d) != 137:
                                                                                                error(message('MATLAB:setptr:WrongLengthFile'))
                                                                                            d[length(d)]=[]
# scrollplot.m:1745
                                                                                        else:
                                                                                            if 'forbidden' == curs:
                                                                                                d=concat(['07C01FF03838703C607CC0E6C1C6C386C706CE067C0C781C38381FF007C00000','1FF03FF87FFCF87EF0FFE1FFE3EFE7CFEF8FFF0FFE1FFC3E7FFC3FF81FF00FE0','00070007']).T
# scrollplot.m:1747
                                                                                            else:
                                                                                                Data_=cellarray(['Pointer',curs])
# scrollplot.m:1751
                                                                                                if logical_not(stringflag):
                                                                                                    set(fig,Data_[arange()])
                                                                                                if nargout > 0:
                                                                                                    varargout[1]=Data_
# scrollplot.m:1753
                                                                                                return varargout
    
    if mac_curs:
        ind=find(d <= '9')
# scrollplot.m:1758
        d[ind]=d(ind) - '0'
# scrollplot.m:1759
        ind=find(d >= 'A')
# scrollplot.m:1760
        d[ind]=d(ind) - 'A' + 10
# scrollplot.m:1761
        bitmap=d(arange(1,64))
# scrollplot.m:1762
        bitmap=dec2bin(bitmap,4) - '0'
# scrollplot.m:1763
        bitmap=reshape(bitmap.T,16,16).T
# scrollplot.m:1764
        mask=d(arange(65,128))
# scrollplot.m:1765
        mask=dec2bin(mask,4) - '0'
# scrollplot.m:1766
        mask=reshape(mask.T,16,16).T
# scrollplot.m:1767
        ind=mask == 0
# scrollplot.m:1768
        mask[ind]=NaN
# scrollplot.m:1769
        cdata=- (- mask + bitmap - 1)
# scrollplot.m:1771
        hotspot_h=d(arange(129,132))
# scrollplot.m:1773
        hotspot_h=dot(16.0 ** (arange(3,0,- 1)),hotspot_h)
# scrollplot.m:1774
        hotspot_v=d(arange(133,136))
# scrollplot.m:1775
        hotspot_v=dot(16.0 ** (arange(3,0,- 1)),hotspot_v)
# scrollplot.m:1776
        hotspot=concat([hotspot_h,hotspot_v]) + 1
# scrollplot.m:1778
    
    Data_=cellarray(['Pointer','custom','PointerShapeCData',cdata,'PointerShapeHotSpot',hotspot])
# scrollplot.m:1781
    if logical_not(stringflag):
        set(fig,Data_[arange()])
    
    if nargout > 0:
        varargout[1]=Data_
# scrollplot.m:1786
    
    #end  # setptr  ##ok for Matlab 6 compatibility
    
    ##################################  TODO  ###################################
# - maybe add a blue diamond or a visual handle in center of side-bars?
# - fix or bypass Matlab 6 OpenGL warning due to patch FaceAlpha property