# Generated with SMOP  0.41
from libsmop import *
# wmean.m

    
@function
def wmean(x=None,w=None,dim=None,*args,**kwargs):
    varargin = wmean.varargin
    nargin = wmean.nargin

    #WMEAN   Weighted Average or mean value.
#   For vectors, WMEAN(X,W) is the weighted mean value of the elements in X
#   using non-negative weights W. For matrices, WMEAN(X,W) is a row vector 
#   containing the weighted mean value of each column.  For N-D arrays, 
#   WMEAN(X,W) is the weighted mean value of the elements along the first 
#   non-singleton dimension of X.
    
    #   Each element of X requires a corresponding weight, and hence the size 
#   of W must match that of X.
    
    #   WMEAN(X,W,DIM) takes the weighted mean along the dimension DIM of X.
    
    #   Class support for inputs X and W:
#      float: double, single
    
    #   Example:
#       x = rand(5,2);
#       w = rand(5,2);
#       wmean(x,w)
    
    if nargin < 2:
        error('Not enough input arguments.')
    
    # Check that dimensions of X match those of W.
    if (logical_not(isequal(size(x),size(w)))):
        error('Inputs x and w must be the same size.')
    
    # Check that all of W are non-negative.
    if (any(ravel(w) < 0)):
        error('All weights, W, must be non-negative.')
    
    # Check that there is at least one non-zero weight.
    if (all(ravel(w) == 0)):
        error('At least one weight must be non-zero.')
    
    if nargin == 2:
        dim=min(find(size(x) != 1))
# wmean.m:43
        if isempty(dim):
            dim=1
# wmean.m:44
    
    y=sum(multiply(w,x),dim) / sum(w,dim)
# wmean.m:47