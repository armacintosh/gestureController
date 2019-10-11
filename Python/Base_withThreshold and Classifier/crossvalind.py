# Generated with SMOP  0.41
from libsmop import *
# crossvalind.m

    
@function
def crossvalind(method=None,N=None,varargin=None,*args,**kwargs):
    varargin = crossvalind.varargin
    nargin = crossvalind.nargin

    #CROSSVALIND generates cross-validation indices
    
    #   INDICES = CROSSVALIND('Kfold',N,K) returns randomly generated indices
#   for a K-fold cross-validation of N observations. INDICES contains equal
#   (or approximately equal) proportions of the integers 1 through K that
#   define a partition of the N observations into K disjoint subsets.
#   Repeated calls return different randomly generated partitions. K
#   defaults to 5 when omitted. In K-fold cross-validation, K-1 folds are
#   used for training and the last fold is used for evaluation. This
#   process is repeated K times, leaving one different fold for evaluation
#   each time.
    
    #   [TRAIN,TEST] = CROSSVALIND('HoldOut',N,P) returns logical index vectors
#   for cross-validation of N observations by randomly selecting P*N
#   (approximately) observations to hold out for the evaluation set. P must
#   be a scalar between 0 and 1. P defaults to 0.5 when omitted,
#   corresponding to holding 50# out. Using holdout cross-validation within
#   a loop is similar to K-fold cross-validation one time outside the loop,
#   except that non-disjointed subsets are assigned to each evaluation.
    
    #   [TRAIN,TEST] = CROSSVALIND('LeaveMOut',N,M), where M is an integer,
#   returns logical index vectors for cross-validation of N observations by
#   randomly selecting M of the observations to hold out for the evaluation
#   set. M defaults to 1 when omitted. Using LeaveMOut cross-validation
#   within a loop does not guarantee disjointed evaluation sets. Use K-fold
#   instead.
    
    #   [TRAIN,TEST] = CROSSVALIND('Resubstitution',N,[P,Q]) returns logical
#   index vectors of indices for cross-validation of N observations by
#   randomly selecting P*N observations for the evaluation set and Q*N
#   observations for training. Sets are selected in order to minimize the
#   number of observations that are used in both sets. P and Q are scalars
#   between 0 and 1. Q=1-P corresponds to holding out (100*P)#, while P=Q=1
#   corresponds to full resubstitution. [P,Q] defaults to [1,1] when omitted.
    
    #   [...] = CROSSVALIND(METHOD,GROUP,...) takes the group structure of the
#   data into account. GROUP is a grouping vector that defines the class for
#   each observation. GROUP can be a numeric vector, a string array, or a
#   cell array of strings. The partition of the groups depends on the type
#   of cross-validation: For K-fold, each group is divided into K subsets,
#   approximately equal in size. For all others, approximately equal
#   numbers of observations from each group are selected for the evaluation
#   set. In both cases the training set will contain at least one
#   observation from each group.
    
    #   [...] = CROSSVALIND(METHOD,GROUP,...,'CLASSES',C) restricts the
#   observations to only those values specified in C.  C can be a numeric
#   vector, a string array, or a cell array of strings, but it is of the
#   same form as GROUP. If one output argument is specified, it will
#   contain the value 0 for observations belonging to excluded classes. If
#   two output arguments are specified, both will contain the logical value
#   false for observations belonging to excluded classes.
    
    #   [...] = CROSSVALIND(METHOD,GROUP,...,'MIN',MIN) sets the minimum number
#   of observations that each group has in the training set. MIN defaults
#   to 1. Setting a large value for MIN can help to balance the training
#   groups, but adds partial resubstitution when there are not enough
#   observations. You cannot set MIN when using K-fold cross-validation.
    
    #   Examples:
    
    #      # Create a 10-fold cross-validation to compute classification error.
#      load fisheriris
#      indices = crossvalind('Kfold',species,10);
#      cp = classperf(species);
#      for i = 1:10
#          test = (indices == i); train = ~test;
#          class = classify(meas(test,:),meas(train,:),species(train,:));
#          classperf(cp,class,test)
#      end
#      cp.ErrorRate
    
    #      # Approximate a leave-one-out prediction error estimate.
#      load carbig
#      x = Displacement; y = Acceleration;
#      N = length(x);
#      sse = 0;
#      for i = 1:100
#          [train,test] = crossvalind('LeaveMOut',N,1);
#          yhat = polyval(polyfit(x(train),y(train),2),x(test));
#          sse = sse + sum((yhat - y(test)).^2);
#      end
#      CVerr = sse / 100
    
    #      # Divide cancer data 60/40 without using the 'Benign' observations.
#      # Assume groups are the true labels of the observations.
#      labels = {'Cancer','Benign','Control'};
#      groups = labels(ceil(rand(100,1)*3));
#      [train,test] = crossvalind('holdout',groups,0.6,'classes',...
#          {'Control','Cancer'});
#      sum(test) # Total groups allocated for testing
#      sum(train) # Total groups allocated for training
    
    #   See also CLASSPERF, CLASSIFY, GRP2IDX, KNNCLASSIFY, SVMCLASSIFY.
    
    #   References:
#   [1] Hastie, T. Tibshirani, R, and Friedman, J. (2001) The Elements of
#       Statistical Learning, Springer, pp. 214-216.
#   [2] Theodoridis, S. and Koutroumbas, K.  (1999) Pattern Recognition,
#       Academic Press, pp. 341-342.
    
    # Copyright 2003-2005 The MathWorks, Inc.
# $Revision: 1.1.10.3 $  $Date: 2005/12/12 23:11:55 $
    
    # set defaults
    classesProvided=copy(false)
# crossvalind.m:107
    MG=1
# crossvalind.m:108
    
    P=0.5
# crossvalind.m:109
    
    K=5
# crossvalind.m:110
    
    M=1
# crossvalind.m:111
    
    Q=concat([1,1])
# crossvalind.m:112
    
    # get and validate the method (first input)
    if ischar(method) and size(method,1) == 1:
        validMethods=cellarray(['holdout','kfold','resubstitution','leavemout'])
# crossvalind.m:116
        method=strmatch(lower(method),validMethods)
# crossvalind.m:117
        if isempty(method):
            error('Bioinfo:crossvalind:NotValidMethod','Not a valid method.')
        method=validMethods[method]
# crossvalind.m:122
    else:
        error('Bioinfo:crossvalind:NotValidTypeForMethod','Valid methods are 'KFold', 'HoldOut', 'LeaveMOut', or 'Resubstitution'.')
    
    if nargout > 1 and isequal(method,'kfold'):
        error('Bioinfo:crossvalind:TooManyOutputArgumentsForKfold','To many output arguments for Kfold cross-validation.')
    
    # take P,K,Q, or M if provided by the third input (first varargin) and
# validate it
    if numel(varargin) and isnumeric(varargin[1]):
        S=varargin[1]
# crossvalind.m:136
        varargin[1]=[]
# crossvalind.m:137
        if 'holdout' == method:
            if numel(S) == 1 and S > 0 and S < 1:
                P=copy(S)
# crossvalind.m:141
            else:
                error('Bioinfo:crossvalind:InvalidThirdInputP','For hold-out cross-validation, the third input must be a scalar between 0 and 1.')
        else:
            if 'kfold' == method:
                if numel(S) == 1 and S >= 1:
                    K=round(S)
# crossvalind.m:148
                else:
                    error('Bioinfo:crossvalind:InvalidThirdInputK','For Kfold cross-validation, the third input must be a positive integer.')
            else:
                if 'leavemout' == method:
                    if numel(S) == 1 and S >= 1:
                        M=round(S)
# crossvalind.m:155
                    else:
                        error('Bioinfo:crossvalind:InvalidThirdInputM','For leave-M-out cross-validation, the third input must be a positive integer.')
                else:
                    if 'resubstitution' == method:
                        if numel(S) == 2 and all(S > 0) and all(S <= 1):
                            Q=ravel(S)
# crossvalind.m:162
                        else:
                            error('Bioinfo:crossvalind:InvalidThirdInputQ','For resubstitution cross-validation, the third input must be a 2x1 vector with values between 0 and 1.')
    
    # read optional paired input arguments in
    if numel(varargin):
        if rem(numel(varargin),2):
            error('Bioinfo:crossvalind:IncorrectNumberOfArguments','Incorrect number of arguments to %s.',mfilename)
        okargs=cellarray(['classes','min'])
# crossvalind.m:176
        for j in arange(1,numel(varargin),2).reshape(-1):
            pname=varargin[j]
# crossvalind.m:178
            pval=varargin[j + 1]
# crossvalind.m:179
            k=strmatch(lower(pname),okargs)
# crossvalind.m:180
            if isempty(k):
                error('Bioinfo:crossvalind:UnknownParameterName','Unknown parameter name: %s.',pname)
            else:
                if length(k) > 1:
                    error('Bioinfo:crossvalind:AmbiguousParameterName','Ambiguous parameter name: %s.',pname)
                else:
                    if 1 == (k):
                        classesProvided=copy(true)
# crossvalind.m:190
                        classes=copy(pval)
# crossvalind.m:191
                    else:
                        if 2 == (k):
                            MG=round(pval(1))
# crossvalind.m:193
                            if MG < 0:
                                error('Bioinfo:crossvalind:NotValidMIN','MIN must be a positive scalar.')
    
    if isscalar(N) and isnumeric(N):
        if N < 1 or N != floor(N):
            error('Bioinfo:crossvalind:NNotPositiveInteger','The number of observations must be a positive integer.')
        group=ones(N,1)
# crossvalind.m:208
    else:
        group,groupNames=grp2idx(N,nargout=2)
# crossvalind.m:210
        N=numel(group)
# crossvalind.m:211
    
    if classesProvided:
        orgN=copy(N)
# crossvalind.m:215
        dummy,classes=grp2idx(classes,nargout=2)
# crossvalind.m:217
        validGroups=intersect(classes,groupNames)
# crossvalind.m:218
        if isempty(validGroups):
            error('bioinfo:crossvalind:EmptyValidGroups','Could not find any valid group. Are CLASSES the same type as GROUP ?')
        selectedGroups=ismember(groupNames(group),validGroups)
# crossvalind.m:223
        group=grp2idx(group(selectedGroups))
# crossvalind.m:224
        N=numel(group)
# crossvalind.m:225
    
    nS=accumarray(ravel(group),1)
# crossvalind.m:228
    if min(nS) < MG:
        error('Bioinfo:crossvalind:MissingObservations','All the groups must have at least least MIN obeservation(s).')
    
    if cellarray(['leavemout','holdout','resubstitution']) == method:
        if 'leavemout' == method:
            # number of samples for holdout in every group
            nSE=repmat(M,numel(nS),1)
# crossvalind.m:239
            nST=max(nS - nSE,MG)
# crossvalind.m:241
        else:
            if 'holdout' == method:
                # computes the number of samples for holdout in every group
                nSE=floor(dot(nS,P))
# crossvalind.m:244
                nST=max(nS - nSE,MG)
# crossvalind.m:246
            else:
                if 'resubstitution' == method:
                    # computes the number of samples for training and evaluation
                    nSE=floor(dot(nS,Q(1)))
# crossvalind.m:249
                    nST=floor(dot(nS,Q(2)))
# crossvalind.m:250
                    nST=max(nST,MG)
# crossvalind.m:252
        # Initializing the outputs
        tInd=false(N,1)
# crossvalind.m:255
        eInd=false(N,1)
# crossvalind.m:256
        for g in arange(1,numel(nS)).reshape(-1):
            h=find(group == g)
# crossvalind.m:259
            randInd=randperm(nS(g))
# crossvalind.m:260
            tInd[h(randInd(arange(1,nST(g))))]=true
# crossvalind.m:261
            eInd[h(randInd(arange(end() - nSE(g) + 1,end())))]=true
# crossvalind.m:262
    else:
        if 'kfold' == method:
            tInd=zeros(N,1)
# crossvalind.m:265
            for g in arange(1,numel(nS)).reshape(-1):
                h=find(group == g)
# crossvalind.m:267
                q=ceil(dot(K,(arange(1,nS(g)))) / nS(g))
# crossvalind.m:269
                pq=randperm(K)
# crossvalind.m:271
                randInd=randperm(nS(g))
# crossvalind.m:273
                tInd[h(randInd)]=pq(q)
# crossvalind.m:274
    
    if classesProvided:
        if isequal(method,'kfold'):
            temp=zeros(orgN,1)
# crossvalind.m:280
            temp[selectedGroups]=tInd
# crossvalind.m:281
            tInd=copy(temp)
# crossvalind.m:282
        else:
            temp=false(orgN,1)
# crossvalind.m:284
            temp[selectedGroups]=tInd
# crossvalind.m:285
            tInd=copy(temp)
# crossvalind.m:286
            temp=false(orgN,1)
# crossvalind.m:287
            temp[selectedGroups]=eInd
# crossvalind.m:288
            eInd=copy(temp)
# crossvalind.m:289
    