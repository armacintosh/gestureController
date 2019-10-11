# Generated with SMOP  0.41
from libsmop import *
# compute_accuracy_F.m

    
@function
def compute_accuracy_F(actual=None,pred=None,classes=None,*args,**kwargs):
    varargin = compute_accuracy_F.varargin
    nargin = compute_accuracy_F.nargin

    # Modified by иЇзг(www.shamoxia.com) from:
# GETCM : gets confusion matrices, precision, recall, and F scores
# [confus,numcorrect,precision,recall,F] = getcm (actual,pred,[classes])
    
    # actual is a N-element vector representing the actual classes
# pred is a N-element vector representing the predicted classes
# classes is a vector with the numbers of the classes (by default, it is 1:k, where k is the
#    largest integer to appear in actual or pred.
    
    # dinoj@cs.uchicago.edu , Apr 2005, modified July 2005
    
    if size(actual,1) != size(pred,1):
        pred=pred.T
# compute_accuracy_F.m:14
    
    if nargin < 3:
        classes=concat([arange(1,max(max(actual),max(pred)))])
# compute_accuracy_F.m:17
    
    ##
    PatN=[]
# compute_accuracy_F.m:21
    MAP=0
# compute_accuracy_F.m:22
    NDCGatN=[]
# compute_accuracy_F.m:23
    num_corr=0
# compute_accuracy_F.m:24
    sum_cp=0
# compute_accuracy_F.m:25
    for i in arange(1,length(actual)).reshape(-1):
        if actual(i) == pred(i):
            num_corr=num_corr + 1
# compute_accuracy_F.m:29
            sum_cp=sum_cp + num_corr / i
# compute_accuracy_F.m:30
        PatN[i]=num_corr / i
# compute_accuracy_F.m:32
    
    if num_corr != 0:
        MAP=sum_cp / num_corr
# compute_accuracy_F.m:35
    
    ##
    
    numcorrect=sum(actual == pred)
# compute_accuracy_F.m:39
    accuracy=numcorrect / length(actual)
# compute_accuracy_F.m:40
    for i in arange(1,length(classes)).reshape(-1):
        # confus(i,:) = hist(pred,classes);
        a=classes(i)
# compute_accuracy_F.m:43
        d=find(actual == a)
# compute_accuracy_F.m:44
        for j in arange(1,length(classes)).reshape(-1):
            confus[i,j]=length(find(pred(d) == classes(j)))
# compute_accuracy_F.m:46
    
    precision=[]
# compute_accuracy_F.m:50
    recall=[]
# compute_accuracy_F.m:51
    F=[]
# compute_accuracy_F.m:52
    for i in arange(1,length(classes)).reshape(-1):
        S=sum(confus(i,arange()))
# compute_accuracy_F.m:56
        if nargout >= 4:
            if S:
                recall[i]=confus(i,i) / sum(confus(i,arange()))
# compute_accuracy_F.m:59
            else:
                recall[i]=0
# compute_accuracy_F.m:61
        S=sum(confus(arange(),i))
# compute_accuracy_F.m:64
        if nargout >= 3:
            if S:
                precision[i]=confus(i,i) / S
# compute_accuracy_F.m:67
            else:
                precision[i]=0
# compute_accuracy_F.m:69
        if nargout >= 5:
            if (precision(i) + recall(i)):
                F[i]=dot(2,(dot(precision(i),recall(i)))) / (precision(i) + recall(i))
# compute_accuracy_F.m:74
            else:
                F[i]=0
# compute_accuracy_F.m:76
    