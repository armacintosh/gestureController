# Generated with SMOP  0.41
from libsmop import *
# StaticAnalysis_RandomForest_setup.m

    
@function
def StaticAnalysis_RandomForest_setup(FtTbl=None,topPercent=None,*args,**kwargs):
    varargin = StaticAnalysis_RandomForest_setup.varargin
    nargin = StaticAnalysis_RandomForest_setup.nargin

    ## Scale the features
    FtTblNorm=copy(FtTbl)
# StaticAnalysis_RandomForest_setup.m:4
    # edit TrueLabel so it is not normalized
    FtTblNorm.TrueLabel = copy(FtTbl.TrueLabel)
# StaticAnalysis_RandomForest_setup.m:7
    # remove NAN cols.
    FtTblNorm=FtTblNorm(arange(),logical_not(any(ismissing(FtTblNorm))))
# StaticAnalysis_RandomForest_setup.m:10
    
    ## separates predictor and response data
    
    inputTable=copy(FtTblNorm)
# StaticAnalysis_RandomForest_setup.m:14
    predictorNames=inputTable.Properties.VariableNames(arange(),arange(2,end()))
# StaticAnalysis_RandomForest_setup.m:15
    
    predictors=inputTable(arange(),predictorNames)
# StaticAnalysis_RandomForest_setup.m:16
    response=inputTable.TrueLabel
# StaticAnalysis_RandomForest_setup.m:17
    ## PCA - goes here if desired
    
    PCADetails=[]
# StaticAnalysis_RandomForest_setup.m:21
    ## separate data into training (60), validation (20) and test sets (20)
    
    # DOES NOT DO CV thus use all data and OBB is the generalization
    TrainingPredictors=table2array(predictors)
# StaticAnalysis_RandomForest_setup.m:26
    TrainingResponse=copy(response)
# StaticAnalysis_RandomForest_setup.m:27
    ## Random Forest classification
    
    # Bootstrap-aggregated (bagged) decision trees
# TreeBagger selects a random subset of predictors to use at each decision split as in the random forest algorithm [1].
# [1] Breiman, L. Random Forests. Machine Learning 45, pp. 5–32, 2001.
    
    NumTrees=200
# StaticAnalysis_RandomForest_setup.m:35
    
    Mdl=TreeBagger(NumTrees,TrainingPredictors,TrainingResponse,'Method','classification','Prior','Empirical','OOBPredictorImportance','on','Surrogate','on','PredictorSelection','interaction-curvature')
# StaticAnalysis_RandomForest_setup.m:36
    ##  evaluate best model on TestSet with the Use the best hyperparameters
    
    pred=oobPredict(Mdl)
# StaticAnalysis_RandomForest_setup.m:49
    
    err=oobError(Mdl)
# StaticAnalysis_RandomForest_setup.m:50
    ## store output
    Output=struct('InputFile',FtTbl,'PCA',PCADetails,'TestingModel',Mdl,'oobError',err)
# StaticAnalysis_RandomForest_setup.m:53
    ##  Importance table
    
    # importance
    FeatureName=FtTblNorm.Properties.VariableNames(arange(2,end()))
# StaticAnalysis_RandomForest_setup.m:62
    importance=Output.TestingModel.OOBPermutedPredictorDeltaError
# StaticAnalysis_RandomForest_setup.m:63
    ImpTable=array2table(importance.T)
# StaticAnalysis_RandomForest_setup.m:65
    ImpTable.Properties.VariableNames = copy(cellarray(['Importance']))
# StaticAnalysis_RandomForest_setup.m:66
    ImpTable.FeatureName = copy(FeatureName.T)
# StaticAnalysis_RandomForest_setup.m:67
    ImpTable,Ind=sortrows(ImpTable,cellarray(['Importance']),cellarray(['descend']),nargout=2)
# StaticAnalysis_RandomForest_setup.m:68
    # number of ft. to include (90/95# of error);
    B=ImpTable.Importance
# StaticAnalysis_RandomForest_setup.m:71
    indkp=find(B < prctile(B,topPercent),1)
# StaticAnalysis_RandomForest_setup.m:72
    
    N=ImpTable.FeatureName
# StaticAnalysis_RandomForest_setup.m:74
    FtTblTop=FtTbl(arange(),N(arange(1,indkp)))
# StaticAnalysis_RandomForest_setup.m:75
    
    indTop=Ind(arange(1,indkp)) + 1
# StaticAnalysis_RandomForest_setup.m:76
    
    FtTblTop.TrueLabel = copy(FtTbl.TrueLabel)
# StaticAnalysis_RandomForest_setup.m:77
    
    # add to function ouput
    Output.ImpTable = copy(ImpTable)
# StaticAnalysis_RandomForest_setup.m:80
    Output.FtTblTop = copy(FtTblTop)
# StaticAnalysis_RandomForest_setup.m:81
    Output.indkpTop = copy(indTop)
# StaticAnalysis_RandomForest_setup.m:82