# Generated with SMOP  0.41
from libsmop import *
# Review_GamePlayThresholds_Now.m

    
@function
def Review_GamePlayThresholds_Now(*args,**kwargs):
    varargin = Review_GamePlayThresholds_Now.varargin
    nargin = Review_GamePlayThresholds_Now.nargin

    # Review_GamePlayThresholds
    
    #     goal is to:
#         find the best RatioE and RatioF 
#         find the aboveBaseE and aboveBaseF
    
    ## input for participant ID and E and F cutoff
    
    ## Select participant
    
    #Options
    option=concat([cellarray(['F01']),cellarray(['F02']),cellarray(['F03']),cellarray(['F04']),cellarray(['F05']),cellarray(['F06']),cellarray(['F07']),cellarray(['F08']),cellarray(['F09']),cellarray(['F10']),cellarray(['AM']),cellarray(['P12']),cellarray(['P43']),cellarray(['P52']),cellarray(['P63']),cellarray(['P81']),cellarray(['P84']),cellarray(['P96']),cellarray(['P97']),cellarray(['P98']),cellarray(['A']),cellarray(['B']),cellarray(['C']),cellarray(['D']),cellarray(['E']),cellarray(['F']),cellarray(['G'])])
# Review_GamePlayThresholds_Now.m:14
    # get user to select gesture code 1 or 2
    s,__=listdlg('PromptString','Select Participant','SelectionMode','single','ListSize',concat([200,100]),'ListString',option,nargout=2)
# Review_GamePlayThresholds_Now.m:45
    participant=option[s]
# Review_GamePlayThresholds_Now.m:50
    ##
    
    # choosing 10 means: 
#     anything above 10#ile peak extension is accepted as extending
#     anything below 90#ile peak flexor activity during extension is accepted as extending
#     increasing from 10 to 20 means it requires more extensor and less flexor activity to be considered extending
#     generally start at 10 and 10
    
    cutoffE=10
# Review_GamePlayThresholds_Now.m:60
    
    cutoffF=10
# Review_GamePlayThresholds_Now.m:61
    
    cutoffGyroRes=10
# Review_GamePlayThresholds_Now.m:62
    
    getweekGroupPlayStats='n'
# Review_GamePlayThresholds_Now.m:63
    
    drawPlot='y'
# Review_GamePlayThresholds_Now.m:64
    
    # Note = inputdlg({
#                 'Enter #ile of mavE peaks to be ACCEPTED (0-100), usually 10-30',...
#                 'Enter #ile of mavF peaks to be REJECTED (0-100), usually 10-30',...
#                 'Enter #ile of MaxGyro peaks to be REJECTED (0-100), usually 10-30',...
#                 'get weekGroupPlayStats? y or n',...
#                 'Draw a Plot for each trial? y or n'},...
#                 'Inputs for Threshold check', [1 100; 1 100; 1 100; 1 100; 1 100]);
# 
# # participant = Note{1};
# cutoffE = str2num(Note{1});
# cutoffF = str2num(Note{2}); 
# cutoffGyroRes = str2num(Note{3});
# getweekGroupPlayStats = Note{4};
# drawPlot = Note{5};
# 
# if isempty(cutoffE)
#     cutoffE = 10; # you want everything > the cutoffE #ile of mavE peaks to be accepted (0-100) 0 easier / maybe too easy
# end
# if isempty(cutoffF)
#     cutoffF = 10; # you want everything > the cutoffE #ile of mavE peaks to be accepted (0-100) 0 easier / maybe too easy
# end
# if isempty(cutoffGyroRes)
#     cutoffGyroRes = 10;
# end
# if isempty(getweekGroupPlayStats)   
#     getweekGroupPlayStats = 'n';
# end
# if isempty(drawPlot)   
#     drawPlot = 'y';
# end
    
    ## move all files to same folder
    
    if getweekGroupPlayStats == 'y':
        ##
        # get the root results folder
        rootResultsFolder=uigetdir('RESULTS FOLDER LOCATION')
# Review_GamePlayThresholds_Now.m:103
        filesConst=dir(strcat(rootResultsFolder,'\**\trialConst_*.mat'))
# Review_GamePlayThresholds_Now.m:106
        filesTrialData=dir(strcat(rootResultsFolder,'\**\trialData_*.txt'))
# Review_GamePlayThresholds_Now.m:107
        mkdir(strcat(rootResultsFolder,'\weekGroupPlayStats'))
        saveFolder=strcat(rootResultsFolder,'\weekGroupPlayStats')
# Review_GamePlayThresholds_Now.m:111
        ConstNames=cellarray([filesConst.name]).T
# Review_GamePlayThresholds_Now.m:114
        C=erase(ConstNames,'trialConst_')
# Review_GamePlayThresholds_Now.m:115
        C=erase(C,'.mat')
# Review_GamePlayThresholds_Now.m:116
        # remove the same in the trialData
        TrialNames=cellarray([filesTrialData.name]).T
# Review_GamePlayThresholds_Now.m:119
        T=erase(TrialNames,'trialData_')
# Review_GamePlayThresholds_Now.m:120
        T=erase(T,'.txt')
# Review_GamePlayThresholds_Now.m:121
        # find the index of filesTrialData that match each C
        __,matchInd=ismember(ravel(C),ravel(T),nargout=2)
# Review_GamePlayThresholds_Now.m:124
        filesTrialDataUse=filesTrialData(matchInd)
# Review_GamePlayThresholds_Now.m:126
        ## copyfiles filesTrialDataUse and corresponding constData to saveFolder
        for f in arange(1,numel(filesTrialDataUse)).reshape(-1):
            # move trialData files
            s=strcat(filesTrialDataUse(f).folder,'\',filesTrialDataUse(f).name)
# Review_GamePlayThresholds_Now.m:134
            d=strcat(saveFolder,'\',filesTrialDataUse(f).name)
# Review_GamePlayThresholds_Now.m:135
            copyfile(s,d)
            sc=strcat(filesConst(f).folder,'\',filesConst(f).name)
# Review_GamePlayThresholds_Now.m:139
            dc=strcat(saveFolder,'\',filesConst(f).name)
# Review_GamePlayThresholds_Now.m:140
            copyfile(sc,dc)
        ##
    
    
    ## Select files
    
    # # go to a participant and pick all trialData
    formatOutFolder='yyyymmdd'
# Review_GamePlayThresholds_Now.m:151
    
    date=datestr(now,formatOutFolder)
# Review_GamePlayThresholds_Now.m:152
    formatOutFolder1='yyyy mm dd'
# Review_GamePlayThresholds_Now.m:154
    
    date1=datestr(now,formatOutFolder1)
# Review_GamePlayThresholds_Now.m:155
    if getweekGroupPlayStats == 'y':
        resultsfolder=copy(saveFolder)
# Review_GamePlayThresholds_Now.m:158
    else:
        resultsfolder=strcat('Results\',date1,'\trialData\')
# Review_GamePlayThresholds_Now.m:160
    
    trialoutput_file,trialoutput_path,ext=uigetfile(strcat(resultsfolder,'\*.txt'),'Select 1 or more "trialData_" files, > 50 KB ','multiselect','on',nargout=3)
# Review_GamePlayThresholds_Now.m:163
    # remove files that dont have a const... or make analysis work without const file...
    if class_(trialoutput_file) == 'cell':
        trialoutput_file=sort(trialoutput_file)
# Review_GamePlayThresholds_Now.m:167
    else:
        # turn single string into cell 1x1
        trialoutput_file=cellarray([trialoutput_file])
# Review_GamePlayThresholds_Now.m:170
    
    ##
## for each trial
    for t in arange(1,length(trialoutput_file)).reshape(-1):
        ## Load data
        # load trial data
        loadthis=strcat(trialoutput_path,trialoutput_file(t))
# Review_GamePlayThresholds_Now.m:180
        trialData=loadTrialData(char(loadthis))
# Review_GamePlayThresholds_Now.m:182
        # there should always be a const file associated with a trial file
        constfile=strrep(trialoutput_file(t),'trialData','trialConst')
# Review_GamePlayThresholds_Now.m:186
        constfile=strrep(constfile,'txt','mat')
# Review_GamePlayThresholds_Now.m:187
        loadconst=strcat(trialoutput_path,constfile)
# Review_GamePlayThresholds_Now.m:188
        const=load(char(loadconst))
# Review_GamePlayThresholds_Now.m:189
        const=const.const
# Review_GamePlayThresholds_Now.m:190
        t_id=char(trialoutput_file(t))
# Review_GamePlayThresholds_Now.m:193
        t_id=t_id(arange(end() - 7,end() - 4))
# Review_GamePlayThresholds_Now.m:194
        ## calculate ratioE and aboveBaseE
#   raitioE would be activity of a median extenion / base
#   aboveBase would be value that lets 90# of extensions pass, above base
        # first, turn into percent currentMax
        trialData.perE = copy(trialData.mavE / trialData.currentMaxE)
# Review_GamePlayThresholds_Now.m:202
        trialData.perF = copy(trialData.mavF / trialData.currentMaxF)
# Review_GamePlayThresholds_Now.m:203
        trialData.perBaseE = copy(trialData.currentBaseE / trialData.currentMaxE)
# Review_GamePlayThresholds_Now.m:206
        trialData.perBaseF = copy(trialData.currentBaseF / trialData.currentMaxF)
# Review_GamePlayThresholds_Now.m:207
        ##
        # get activity range and peaks above baseline E
    # every mavE should first be a # between base and max...
        perCurrentRng=trialData.currentMaxE - trialData.currentBaseE
# Review_GamePlayThresholds_Now.m:213
        z=trialData.mavE - trialData.currentBaseE
# Review_GamePlayThresholds_Now.m:214
        perAboveBaseE=z / perCurrentRng
# Review_GamePlayThresholds_Now.m:215
        # pick peak indicies of max from z
        peaks.indE,peaks.valPkE=peakseek(perAboveBaseE,const.minpeakdist,std(perAboveBaseE),nargout=2)
# Review_GamePlayThresholds_Now.m:218
        # get the above base that would let most extensions things pass
    # tryig to tell me: const.aboveBaseE for pb3
        minAboveBaseE=prctile(perAboveBaseE(peaks.indE),cutoffE)
# Review_GamePlayThresholds_Now.m:222
        # predicted min E
        out.minE = copy(trialData.currentBaseE + (dot((trialData.currentMaxE - trialData.currentBaseE),minAboveBaseE)))
# Review_GamePlayThresholds_Now.m:225
        # every mavE should first be a # between base and max...
        perCurrentRngF=trialData.currentMaxF - trialData.currentBaseF
# Review_GamePlayThresholds_Now.m:229
        zF=trialData.mavF - trialData.currentBaseF
# Review_GamePlayThresholds_Now.m:230
        perAboveBaseF=zF / perCurrentRngF
# Review_GamePlayThresholds_Now.m:231
        # want activity of flexors duing extension, thus use previous index    
        # get the above base that would let most extensions things pass
        # tryig to tell me: const.aboveBaseF for pb3
        maxAboveBaseF=prctile(perAboveBaseF(peaks.indE),100 - cutoffF)
# Review_GamePlayThresholds_Now.m:236
        # predicted max F
        out.maxF = copy(trialData.currentBaseF + (dot((trialData.currentMaxF - trialData.currentBaseF),maxAboveBaseF)))
# Review_GamePlayThresholds_Now.m:239
        #get Gyro Data
        GyroResPeak=trialData.GyroRes(trialData.pressed == 1)
# Review_GamePlayThresholds_Now.m:245
        out.maxGyroRes = copy(prctile(GyroResPeak,100 - cutoffGyroRes))
# Review_GamePlayThresholds_Now.m:246
        ## plot
        if drawPlot == 'y':
            Review_GamePlayThresholds_Plot(const,t_id,trialData,peaks,out)
        ## store relevant infromation
        # store the abs. vals of the thresh
        result(t).trial = copy(trialoutput_file[t])
# Review_GamePlayThresholds_Now.m:259
        result(t).ID = copy(t_id)
# Review_GamePlayThresholds_Now.m:260
        result(t).const = copy(const)
# Review_GamePlayThresholds_Now.m:261
        result(t).trialData = copy(trialData)
# Review_GamePlayThresholds_Now.m:262
        result(t).cutoffE = copy(cutoffE)
# Review_GamePlayThresholds_Now.m:265
        result(t).cutoffF = copy(cutoffF)
# Review_GamePlayThresholds_Now.m:266
        result(t).cutoffGyroRes = copy(cutoffGyroRes)
# Review_GamePlayThresholds_Now.m:267
        result(1).aboveBaseE_x = copy([])
# Review_GamePlayThresholds_Now.m:270
        result(1).aboveBaseF_x = copy([])
# Review_GamePlayThresholds_Now.m:271
        result(t).aboveBaseE = copy(minAboveBaseE)
# Review_GamePlayThresholds_Now.m:274
        result(t).aboveBaseF = copy(maxAboveBaseF)
# Review_GamePlayThresholds_Now.m:275
        result(t).nPeaks = copy(length(peaks.indE))
# Review_GamePlayThresholds_Now.m:276
        result(t).perAboveBaseE = copy(perAboveBaseE((peaks.indE)))
# Review_GamePlayThresholds_Now.m:279
        result(t).perAboveBaseF = copy(perAboveBaseF((peaks.indE)))
# Review_GamePlayThresholds_Now.m:280
        result(t).perAboveBaseE_x = copy(mean(perAboveBaseE(peaks.indE)))
# Review_GamePlayThresholds_Now.m:281
        result(t).perAboveBaseE_sd = copy(std(perAboveBaseE(peaks.indE)))
# Review_GamePlayThresholds_Now.m:282
        result(t).perAboveBaseF_x = copy(mean(perAboveBaseF(peaks.indE)))
# Review_GamePlayThresholds_Now.m:283
        result(t).perAboveBaseF_sd = copy(std(perAboveBaseF(peaks.indE)))
# Review_GamePlayThresholds_Now.m:284
        result(t).perBaseE_x = copy(mean(trialData.perBaseE))
# Review_GamePlayThresholds_Now.m:287
        result(t).perBaseE_sd = copy(std(trialData.perBaseE))
# Review_GamePlayThresholds_Now.m:288
        result(t).perBaseF_x = copy(mean(trialData.perBaseF))
# Review_GamePlayThresholds_Now.m:289
        result(t).perBaseF_sd = copy(std(trialData.perBaseF))
# Review_GamePlayThresholds_Now.m:290
        result(t).perBaseE = copy(trialData.perBaseE)
# Review_GamePlayThresholds_Now.m:291
        result(t).perBaseF = copy(trialData.perBaseF)
# Review_GamePlayThresholds_Now.m:292
        result(t).minE_pred = copy(out.minE)
# Review_GamePlayThresholds_Now.m:295
        result(t).maxF_pred = copy(out.maxF)
# Review_GamePlayThresholds_Now.m:296
        result(t).maxGyroRes = copy(out.maxGyroRes)
# Review_GamePlayThresholds_Now.m:299
        result(t).nPeaksGyro = copy(length(GyroResPeak))
# Review_GamePlayThresholds_Now.m:300
    
    
    ## Clean result to not include rows with NAN
    
    # None of these can have NAN:  aboveBaseE, aboveBaseF, maxGyroRes
    index=structfind(result,'aboveBaseE',NaN)
# Review_GamePlayThresholds_Now.m:310
    result[index]=[]
# Review_GamePlayThresholds_Now.m:311
    index=structfind(result,'aboveBaseF',NaN)
# Review_GamePlayThresholds_Now.m:313
    result[index]=[]
# Review_GamePlayThresholds_Now.m:314
    index=structfind(result,'maxGyroRes',NaN)
# Review_GamePlayThresholds_Now.m:316
    result[index]=[]
# Review_GamePlayThresholds_Now.m:317
    ##
#  weigthed average of aboveBase E /F for use in constFile.txt
# get # totals of weight (n rows used), based on number of peaks used to set #ile
    all=concat([ravel(result).nPeaks])
# Review_GamePlayThresholds_Now.m:322
    S[arange(),1]=ravel(all) / sum(all)
# Review_GamePlayThresholds_Now.m:323
    E=concat([ravel(result).aboveBaseE]).T
# Review_GamePlayThresholds_Now.m:324
    F=concat([ravel(result).aboveBaseF]).T
# Review_GamePlayThresholds_Now.m:325
    G=concat([ravel(result).maxGyroRes]).T
# Review_GamePlayThresholds_Now.m:326
    # the main extensor sensor overall
    yE=wmean(E,S,1)
# Review_GamePlayThresholds_Now.m:329
    yF=wmean(F,S,1)
# Review_GamePlayThresholds_Now.m:330
    yG=wmean(G,S,1)
# Review_GamePlayThresholds_Now.m:331
    # to suggest and put into constFile.
    result(1).aboveBaseE_x = copy(yE)
# Review_GamePlayThresholds_Now.m:334
    result(1).aboveBaseF_x = copy(yF)
# Review_GamePlayThresholds_Now.m:335
    result(1).maxGyroRes_x = copy(yG)
# Review_GamePlayThresholds_Now.m:336
    
    # Say weather making it easier or harder
    if yE < const.aboveBaseE:
        changedirE=' --> easier'
# Review_GamePlayThresholds_Now.m:342
    else:
        changedirE=' --> harder'
# Review_GamePlayThresholds_Now.m:344
    
    if yF > const.aboveBaseF:
        changedirF=' --> easier'
# Review_GamePlayThresholds_Now.m:348
    else:
        changedirF=' --> harder'
# Review_GamePlayThresholds_Now.m:350
    
    if yG > const.aboveBaseGyro:
        changedirG=' --> easier'
# Review_GamePlayThresholds_Now.m:354
    else:
        changedirG=' --> harder'
# Review_GamePlayThresholds_Now.m:356
    
    strE='aboveBaseE will be changed from:  %.2f,  to:  %.2f , making it %s  \n\n'
# Review_GamePlayThresholds_Now.m:359
    strF='aboveBaseF will be changed from:  %.2f,  to:  %.2f , making it %s  \n\n'
# Review_GamePlayThresholds_Now.m:360
    strG='aboveBaseGyro will be changed from:  %.2f,  to:  %.2f , making it %s  \n\n'
# Review_GamePlayThresholds_Now.m:361
    strAskE='Change aboveBaseE? \n\n'
# Review_GamePlayThresholds_Now.m:362
    strAskF='Change aboveBaseF? \n\n'
# Review_GamePlayThresholds_Now.m:363
    strAskG='Change aboveBaseGyro? \n\n'
# Review_GamePlayThresholds_Now.m:364
    strAll_Final=strcat(strE,strF,strG)
# Review_GamePlayThresholds_Now.m:366
    strE_Final=strcat(strE,strAskE)
# Review_GamePlayThresholds_Now.m:367
    strF_Final=strcat(strF,strAskF)
# Review_GamePlayThresholds_Now.m:368
    strG_Final=strcat(strG,strAskG)
# Review_GamePlayThresholds_Now.m:369
    promptAll=sprintf(strAll_Final,const.aboveBaseE,yE,changedirE,const.aboveBaseF,yF,changedirF,const.aboveBaseGyro,yG,changedirG)
# Review_GamePlayThresholds_Now.m:371
    promptE=sprintf(strE_Final,const.aboveBaseE,yE,changedirE)
# Review_GamePlayThresholds_Now.m:376
    promptF=sprintf(strF_Final,const.aboveBaseF,yF,changedirF)
# Review_GamePlayThresholds_Now.m:379
    promptG=sprintf(strG_Final,const.aboveBaseGyro,yG,changedirG)
# Review_GamePlayThresholds_Now.m:382
    f=msgbox(cellarray([promptAll,'Paused script to view graph(s)']))
# Review_GamePlayThresholds_Now.m:385
    while ishandle(f):

        pause(0.5)

    
    
    
    ## Questions
    
    updateE=0
# Review_GamePlayThresholds_Now.m:393
    updateF=0
# Review_GamePlayThresholds_Now.m:394
    updateG=0
# Review_GamePlayThresholds_Now.m:395
    options.Interpreter = copy('tex')
# Review_GamePlayThresholds_Now.m:398
    # Include the desired Default answer
    options.Default = copy('Don't know')
# Review_GamePlayThresholds_Now.m:400
    # Construct a questdlg with three options for E
    choice=questdlg(promptE,'Update Extensor thresh?','Yes','No',options)
# Review_GamePlayThresholds_Now.m:402
    # Handle response
    if 'Yes' == choice:
        disp(concat([choice,', Updating constFile.txt']))
        updateE=1
# Review_GamePlayThresholds_Now.m:409
    else:
        if 'No' == choice:
            disp(concat([choice,', Keeping constFile.txt']))
            updateE=0
# Review_GamePlayThresholds_Now.m:412
        else:
            if 'Don't know' == choice:
                updateE=0
# Review_GamePlayThresholds_Now.m:414
    
    # Construct a questdlg with three options for F
    choiceF=questdlg(promptF,'Update Flexor thresh?','Yes','No',options)
# Review_GamePlayThresholds_Now.m:419
    # Handle response
    if 'Yes' == choiceF:
        disp(concat([choiceF,', Updating constFile.txt']))
        updateF=1
# Review_GamePlayThresholds_Now.m:426
    else:
        if 'No' == choiceF:
            disp(concat([choiceF,', Keeping constFile.txt']))
            updateF=0
# Review_GamePlayThresholds_Now.m:430
        else:
            if 'Don't know' == choiceF:
                updateF=0
# Review_GamePlayThresholds_Now.m:432
    
    # GYRO Dialgue
# Construct a questdlg with three options for G
    choiceG=questdlg(promptG,'Update Gyro Thresh?','Yes','No',options)
# Review_GamePlayThresholds_Now.m:438
    # Handle response
    if 'Yes' == choiceG:
        disp(concat([choiceG,', Updating constFile.txt']))
        updateG=1
# Review_GamePlayThresholds_Now.m:445
    else:
        if 'No' == choiceG:
            disp(concat([choiceG,', Keeping constFile.txt']))
            updateG=0
# Review_GamePlayThresholds_Now.m:448
        else:
            if 'Don't know' == choiceG:
                updateG=0
# Review_GamePlayThresholds_Now.m:450
    
    ## this should update const.Low or const.minE
    
    # replace in constFile.txt, w strfind.
    if updateE == 1 or updateF == 1 or updateG == 1:
        # select constfile to open:
        constFileName,constFilePath=uigetfile(strcat('..\..\..',resultsfolder,'*.txt'),'Select constFile.txt to update',nargout=2)
# Review_GamePlayThresholds_Now.m:460
        constfileLoc=strcat(constFilePath,constFileName)
# Review_GamePlayThresholds_Now.m:461
        fid=fopen(constfileLoc,'r')
# Review_GamePlayThresholds_Now.m:464
        f=fread(fid,'*char').T
# Review_GamePlayThresholds_Now.m:465
        fclose(fid)
        if updateE == 1:
            # update the value aboveBaseE
            newStr=strcat('aboveBaseE=',num2str(yE),'; %')
# Review_GamePlayThresholds_Now.m:470
            oldStr=strcat('aboveBaseE=')
# Review_GamePlayThresholds_Now.m:471
            f=strrep(f,oldStr,newStr)
# Review_GamePlayThresholds_Now.m:472
        if updateF == 1:
            # update the value aboveBaseF
            newStr=strcat('aboveBaseF=',num2str(yF),'; %')
# Review_GamePlayThresholds_Now.m:477
            oldStr=strcat('aboveBaseF=')
# Review_GamePlayThresholds_Now.m:478
            f=strrep(f,oldStr,newStr)
# Review_GamePlayThresholds_Now.m:479
        if updateG == 1:
            # update the value aboveBaseF
            newStr=strcat('aboveBaseGyro=',num2str(yG),'; %')
# Review_GamePlayThresholds_Now.m:484
            oldStr=strcat('aboveBaseGyro=')
# Review_GamePlayThresholds_Now.m:485
            f=strrep(f,oldStr,newStr)
# Review_GamePlayThresholds_Now.m:486
        ##    # save
        fid=fopen(constfileLoc,'w')
# Review_GamePlayThresholds_Now.m:490
        fprintf(fid,'%s',f)
        fclose(fid)
        constFileSave1=strcat(trialoutput_path,'constFile.txt')
# Review_GamePlayThresholds_Now.m:495
        copyfile(constfileLoc,constFileSave1)
        constFileStore=strcat(trialoutput_path,'constFile_',participant,'_',date,'.txt')
# Review_GamePlayThresholds_Now.m:498
        copyfile(constfileLoc,constFileStore)
        ##
    
    # keep result used or unused
    result(1).usedUpdate = copy(concat([updateE,updateF,updateG]))
# Review_GamePlayThresholds_Now.m:505
    ## Save
    
    # Store info that may be needed
# save summary info. if required...
    try:
        filename=strcat(trialoutput_path,participant,'_Review_AboveBase_',date,'.mat')
# Review_GamePlayThresholds_Now.m:512
    finally:
        pass
    
    save(filename,'result')
    ## simple printout of stats for therapist
    
    # only want rows with peaks
    result=result(concat([ravel(result).nPeaks]) > 1)
# Review_GamePlayThresholds_Now.m:522
    # get total number of times played
    nPlaySessions=size(ravel(result),1)
# Review_GamePlayThresholds_Now.m:525
    # get total number  of extensions
    nExtensions=sum(concat([ravel(result).nPeaks]))
# Review_GamePlayThresholds_Now.m:528
    nxExtensions=mean(concat([ravel(result).nPeaks]))
# Review_GamePlayThresholds_Now.m:529
    nSDExtensions=std(concat([ravel(result).nPeaks]))
# Review_GamePlayThresholds_Now.m:530
    # get total time playing
    sPlayed=seconds(0)
# Review_GamePlayThresholds_Now.m:533
    for s in arange(1,nPlaySessions).reshape(-1):
        sPlayed=sPlayed + (result(s).trialData.time(end()) - result(s).trialData.time(2))
# Review_GamePlayThresholds_Now.m:535
    
    sPlayed=minutes(sPlayed)
# Review_GamePlayThresholds_Now.m:537
    ##
    
    # setup output string for therapists.
# str0 = strcat('Number of seessions        -->', num2str(nPlaySessions));
# str1 = strcat('Total minutes playing      -->', num2str(round(sPlayed,2)));
# str2 = strcat('Total number of extensions -->', num2str(nExtensions));
# 
# f = msgbox({str0;str1;str2},'\fontsize{15} text');
    
    # ##
# # setup output string for therapists.
# str0 = 'During the session they: \n';
# str1 = '- were activly playing for a total of: #s,  \n';
# str2 = '- extended their wrist a total of: #i times, and \n';
# str3 = '- had an average extension muscle activity of #.2f when extending. \n\n';
# str = strcat(str0, str1, str2, str3);
# 
# # if isstruct(result)
# #     # mean extensor activity while extending - baseline activity (all relative to current max)
# #     # should do this a better way probably reshape with (:)
# #     xExtActivity_1 = result.perAboveBaseE_x;
# #     xExtBase_1 = result.perBaseE_x;
# #     timePlaying = result.trialData.time(end) - result.trialData.time(1);
# #     for trl = 2:length(result)
# #         xExtActivity_1 = vertcat(xExtActivity_1,result(trl).perAboveBaseE);
# #         xExtBase_1 = vertcat(xExtBase_1,result(trl).perBaseE);
# #         timePlaying = timePlaying  + (result(trl).trialData.time(end) - result(trl).trialData.time(1));
# #     end
# #     xExtActivity = mean(xExtActivity_1) - mean(xExtBase_1);    
# #     
# # else
# 
#     # mean extensor activity while extending - baseline activity (all relative to current max)
#     # should do this a better way probably reshape with (:)
#     xExtActivity_1 = result(1).perAboveBaseE;
#     xExtBase_1 = result(1).perBaseE;
#     timePlaying = result(1).trialData.time(end) - result(1).trialData.time(1);
#     
#     for trl = 2:length(result)
#         xExtActivity_1 = vertcat(xExtActivity_1,result(trl).perAboveBaseE);
#         xExtBase_1 = vertcat(xExtBase_1,result(trl).perBaseE);
#         timePlaying = timePlaying  + (result(trl).trialData.time(end) - result(trl).trialData.time(1));
#     end
#     xExtActivity = mean(xExtActivity_1) - mean(xExtBase_1);
# 
# # end
# 
# 
# 
# fprintf(str, char(timePlaying),nExtensions,xExtActivity);
    
    # next would add data from the game / performance
    close_('all')
    # winopen(trialoutput_path);
    