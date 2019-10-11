# Generated with SMOP  0.41
from libsmop import *
# StatisticalAnalysis_SVMGrid_setup.m

    
@function
def StatisticalAnalysis_SVMGrid_setup(FtTbl=None,*args,**kwargs):
    varargin = StatisticalAnalysis_SVMGrid_setup.varargin
    nargin = StatisticalAnalysis_SVMGrid_setup.nargin

    FtTblNorm=copy(FtTbl)
# StatisticalAnalysis_SVMGrid_setup.m:4
    FtTblNorm=sortrows(FtTblNorm,'TrueLabel')
# StatisticalAnalysis_SVMGrid_setup.m:5
    inputTableO[1]=FtTblNorm
# StatisticalAnalysis_SVMGrid_setup.m:7
    ## Classify using SVM Grid search
    
    ClassOutput=cell(size(inputTableO))
# StatisticalAnalysis_SVMGrid_setup.m:11
    for iTbl in arange(1,length(inputTableO)).reshape(-1):
        ## separates predictor and response data
        inputTable=inputTableO[iTbl]
# StatisticalAnalysis_SVMGrid_setup.m:16
        predictorNames=inputTable.Properties.VariableNames(arange(),arange(1,end() - 1))
# StatisticalAnalysis_SVMGrid_setup.m:17
        predictors=inputTable(arange(),predictorNames)
# StatisticalAnalysis_SVMGrid_setup.m:18
        response=inputTable.TrueLabel
# StatisticalAnalysis_SVMGrid_setup.m:19
        ## PCA - goes here if desired
        PCADetails=[]
# StatisticalAnalysis_SVMGrid_setup.m:23
        ## separate data into training (60), validation (20) and test sets (20)
        # Set up holdout validation
        cvp=cvpartition(response,'Holdout',0.2)
# StatisticalAnalysis_SVMGrid_setup.m:28
        trainingPredictors=predictors(cvp.training,arange())
# StatisticalAnalysis_SVMGrid_setup.m:29
        trainingResponse=response(cvp.training,arange())
# StatisticalAnalysis_SVMGrid_setup.m:30
        TestingPredictors=predictors(cvp.test,arange())
# StatisticalAnalysis_SVMGrid_setup.m:31
        TestingResponse=response(cvp.test,arange())
# StatisticalAnalysis_SVMGrid_setup.m:32
        # Optimize hyperperameters within k-fold classification
    # do grid search for hyperparameters on each fold.
        targets=copy(trainingResponse)
# StatisticalAnalysis_SVMGrid_setup.m:39
        kFolds=10
# StatisticalAnalysis_SVMGrid_setup.m:40
        kIdx=crossvalind('Kfold',length(targets),kFolds)
# StatisticalAnalysis_SVMGrid_setup.m:41
        ##
        # setup the output structure
        bestFeatScore=copy(inf)
# StatisticalAnalysis_SVMGrid_setup.m:46
        SVMBest=struct('BestSVMModel',NaN,'BestBoxConstraint',NaN,'BestScore',Inf,'FeaturesIdx',NaN)
# StatisticalAnalysis_SVMGrid_setup.m:48
        SVMHistory=struct('Fold',NaN,'SVMModel',NaN,'LossScores',NaN,'BestBoxConstraint',NaN,'BestScore',Inf)
# StatisticalAnalysis_SVMGrid_setup.m:53
        for k in arange(1,kFolds).reshape(-1):
            # prepare a training set and a validation set for this fold.
            trainData=trainingPredictors(kIdx != k,arange())
# StatisticalAnalysis_SVMGrid_setup.m:62
            trainTarg=targets(kIdx != k)
# StatisticalAnalysis_SVMGrid_setup.m:63
            testData=trainingPredictors(kIdx == k,arange())
# StatisticalAnalysis_SVMGrid_setup.m:64
            testTarg=targets(kIdx == k)
# StatisticalAnalysis_SVMGrid_setup.m:65
            bestCScore=copy(inf)
# StatisticalAnalysis_SVMGrid_setup.m:66
            bestC=copy(NaN)
# StatisticalAnalysis_SVMGrid_setup.m:67
            bestCSVM=copy(NaN)
# StatisticalAnalysis_SVMGrid_setup.m:68
            gridC=2.0 ** (arange(- 5,15,2))
# StatisticalAnalysis_SVMGrid_setup.m:69
            L=ones(1,length(gridC))
# StatisticalAnalysis_SVMGrid_setup.m:70
            for C in gridC.reshape(-1):
                Cind=find(gridC == C)
# StatisticalAnalysis_SVMGrid_setup.m:74
                template=templateSVM('KernelFunction','rbf','PolynomialOrder',[],'KernelScale','auto','BoxConstraint',C,'Standardize',false)
# StatisticalAnalysis_SVMGrid_setup.m:76
                anSVMModel=fitcecoc(trainData,trainTarg,'Learners',template,'Coding','onevsall','ClassNames',unique(targets))
# StatisticalAnalysis_SVMGrid_setup.m:82
                # determine how well the SVM performed:
                L[Cind]=loss(anSVMModel,testData,testTarg)
# StatisticalAnalysis_SVMGrid_setup.m:90
                if L(Cind) < bestCScore:
                    bestCSVM=copy(anSVMModel)
# StatisticalAnalysis_SVMGrid_setup.m:94
                    bestC=copy(C)
# StatisticalAnalysis_SVMGrid_setup.m:95
                    bestCScore=L(Cind)
# StatisticalAnalysis_SVMGrid_setup.m:96
            # for this fold, save the best SVM and its parameters, with all
        # classification errors from gridsearch
            SVMHistory(k).Fold = copy(k)
# StatisticalAnalysis_SVMGrid_setup.m:103
            SVMHistory(k).SVMModel = copy(bestCSVM)
# StatisticalAnalysis_SVMGrid_setup.m:104
            SVMHistory(k).LossScores = copy(L)
# StatisticalAnalysis_SVMGrid_setup.m:105
            SVMHistory(k).BestBoxConstraint = copy(bestC)
# StatisticalAnalysis_SVMGrid_setup.m:106
            SVMHistory(k).BestScore = copy(bestCScore)
# StatisticalAnalysis_SVMGrid_setup.m:107
            if bestCScore < bestFeatScore:
                SVMBest.BestSVMModel = copy(SVMHistory(k).SVMModel)
# StatisticalAnalysis_SVMGrid_setup.m:112
                SVMBest.BestBoxConstraint = copy(SVMHistory(k).BestBoxConstraint)
# StatisticalAnalysis_SVMGrid_setup.m:113
                SVMBest.BestScore = copy(SVMHistory(k).BestScore)
# StatisticalAnalysis_SVMGrid_setup.m:114
        ## Retrain
        # we need to retrain here and save the SVM for the best C
        templateOptim=templateSVM('KernelFunction','rbf','PolynomialOrder',[],'KernelScale','auto','BoxConstraint',SVMBest.BestBoxConstraint,'Standardize',false)
# StatisticalAnalysis_SVMGrid_setup.m:123
        # maybe I can just use the model output from before instead of re-training...?
        Mdl,__=fitcecoc(trainingPredictors,trainingResponse,'Learners',templateOptim,'Coding','onevsall','ClassNames',unique(targets),nargout=2)
# StatisticalAnalysis_SVMGrid_setup.m:131
        ##  evaluate best model on TestSet with the Use the best hyperparameters
        # get predicted labels for final testing set,
        pred=predict(Mdl,TestingPredictors)
# StatisticalAnalysis_SVMGrid_setup.m:142
        confus,accuracy,numcorrect,precision,recall,F,PatN,MAP,NDCGatN=compute_accuracy_F(TestingResponse,pred,unique(TestingResponse),nargout=9)
# StatisticalAnalysis_SVMGrid_setup.m:145
        Labels=num2str(unique(TestingResponse))
# StatisticalAnalysis_SVMGrid_setup.m:147
        Labels=cellstr(Labels)
# StatisticalAnalysis_SVMGrid_setup.m:148
        Labels=strcat('g_',Labels)
# StatisticalAnalysis_SVMGrid_setup.m:149
        confus=array2table(confus)
# StatisticalAnalysis_SVMGrid_setup.m:150
        confus.Properties.VariableNames = copy(Labels)
# StatisticalAnalysis_SVMGrid_setup.m:151
        ClassOutput[iTbl]=struct('InputFile',FtTbl,'PCA',PCADetails,'SVMBest',SVMBest,'SVMHistory',SVMHistory,'TestingModel',Mdl,'ConfusionMat',confus,'Accuracy',accuracy,'Precision',precision,'Recall',recall,'Fscore',F)
# StatisticalAnalysis_SVMGrid_setup.m:154
    