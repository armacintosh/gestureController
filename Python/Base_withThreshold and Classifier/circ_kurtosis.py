# Generated with SMOP  0.41
from libsmop import *
# circ_kurtosis.m

    
@function
def circ_kurtosis(alpha=None,w=None,dim=None,*args,**kwargs):
    varargin = circ_kurtosis.varargin
    nargin = circ_kurtosis.nargin

    # [k k0] = circ_kurtosis(alpha,w,dim)
#   Calculates a measure of angular kurtosis.
    
    #   Input:
#     alpha     sample of angles
#     [w        weightings in case of binned angle data]
#     [dim      statistic computed along this dimension, 1]
    
    #     If dim argument is specified, all other optional arguments can be
#     left empty: circ_kurtosis(alpha, [], dim)
    
    #   Output:
#     k         kurtosis (from Pewsey)
#     k0        kurtosis (from Fisher)
    
    #   References:
#     Pewsey, Metrika, 2004
#     Fisher, Circular Statistics, p. 34
    
    # Circular Statistics Toolbox for Matlab
    
    # By Philipp Berens, 2009
# berens@tuebingen.mpg.de
    
    if nargin < 3:
        dim=1
# circ_kurtosis.m:28
    
    if nargin < 2 or isempty(w):
        # if no specific weighting has been specified
  # assume no binning has taken place
        w=ones(size(alpha))
# circ_kurtosis.m:34
    else:
        if size(w,2) != size(alpha,2) or size(w,1) != size(alpha,1):
            error('Input dimensions do not match')
    
    # compute mean direction
    R=circ_r(alpha,w,[],dim)
# circ_kurtosis.m:42
    theta=circ_mean(alpha,w,dim)
# circ_kurtosis.m:43
    __,rho2=circ_moment(alpha,w,2,true,dim,nargout=2)
# circ_kurtosis.m:44
    __,__,mu2=circ_moment(alpha,w,2,false,dim,nargout=3)
# circ_kurtosis.m:45
    # compute skewness
    theta2=repmat(theta,size(alpha) / size(theta))
# circ_kurtosis.m:48
    k=sum(multiply(w,(cos(dot(2,(circ_dist(alpha,theta2)))))),dim) / sum(w,dim)
# circ_kurtosis.m:49
    k0=(multiply(rho2,cos(circ_dist(mu2,dot(2,theta)))) - R ** 4) / (1 - R) ** 2
# circ_kurtosis.m:50
    