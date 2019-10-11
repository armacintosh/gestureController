# Generated with SMOP  0.41
from libsmop import *
# circ_skewness.m

    
@function
def circ_skewness(alpha=None,w=None,dim=None,*args,**kwargs):
    varargin = circ_skewness.varargin
    nargin = circ_skewness.nargin

    # [b b0] = circ_skewness(alpha,w,dim)
#   Calculates a measure of angular skewness.
    
    #   Input:
#     alpha     sample of angles
#     [w        weightings in case of binned angle data]
#     [dim      statistic computed along this dimension, 1]
    
    #     If dim argument is specified, all other optional arguments can be
#     left empty: circ_skewness(alpha, [], dim)
    
    #   Output:
#     b         skewness (from Pewsey)
#     b0        alternative skewness measure (from Fisher)
    
    #   References:
#     Pewsey, Metrika, 2004
#     Statistical analysis of circular data, Fisher, p. 34
    
    # Circular Statistics Toolbox for Matlab
    
    # By Philipp Berens, 2009
# berens@tuebingen.mpg.de
    
    if nargin < 3:
        dim=1
# circ_skewness.m:28
    
    if nargin < 2 or isempty(w):
        # if no specific weighting has been specified
  # assume no binning has taken place
        w=ones(size(alpha))
# circ_skewness.m:34
    else:
        if size(w,2) != size(alpha,2) or size(w,1) != size(alpha,1):
            error('Input dimensions do not match')
    
    # compute neccessary values
    R=circ_r(alpha,w,[],dim)
# circ_skewness.m:43
    theta=circ_mean(alpha,w,dim)
# circ_skewness.m:44
    __,rho2,mu2=circ_moment(alpha,w,2,true,dim,nargout=3)
# circ_skewness.m:45
    # compute skewness
    theta2=repmat(theta,size(alpha) / size(theta))
# circ_skewness.m:48
    b=sum(multiply(w,(sin(dot(2,(circ_dist(alpha,theta2)))))),dim) / sum(w,dim)
# circ_skewness.m:49
    b0=multiply(rho2,sin(circ_dist(mu2,dot(2,theta)))) / (1 - R) ** (3 / 2)
# circ_skewness.m:50
    