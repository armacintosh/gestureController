# Generated with SMOP  0.41
from libsmop import *
# circ_moment.m

    
@function
def circ_moment(alpha=None,w=None,p=None,cent=None,dim=None,*args,**kwargs):
    varargin = circ_moment.varargin
    nargin = circ_moment.nargin

    # [mp cbar sbar] = circ_moment(alpha, w, p, cent, dim)
#   Calculates the complex p-th centred or non-centred moment 
#   of the angular data in angle.
    
    #   Input:
#     alpha     sample of angles
#     [w        weightings in case of binned angle data]
#     [p        p-th moment to be computed, default is p=1]
#     [cent     if true, central moments are computed, default = false]
#     [dim      compute along this dimension, default is 1]
    
    #     If dim argument is specified, all other optional arguments can be
#     left empty: circ_moment(alpha, [], [], [], dim)
    
    #   Output:
#     mp        complex p-th moment
#     rho_p     magnitude of the p-th moment
#     mu_p      angle of th p-th moment
    
    
    #   References:
#     Statistical analysis of circular data, Fisher, p. 33/34
    
    # Circular Statistics Toolbox for Matlab
    
    # By Philipp Berens, 2009
# berens@tuebingen.mpg.de
    
    if nargin < 5:
        dim=1
# circ_moment.m:32
    
    if nargin < 4:
        cent=copy(false)
# circ_moment.m:36
    
    if nargin < 3 or isempty(p):
        p=1
# circ_moment.m:40
    
    if nargin < 2 or isempty(w):
        # if no specific weighting has been specified
  # assume no binning has taken place
        w=ones(size(alpha))
# circ_moment.m:46
    else:
        if size(w,2) != size(alpha,2) or size(w,1) != size(alpha,1):
            error('Input dimensions do not match')
    
    if cent:
        theta=circ_mean(alpha,w,dim)
# circ_moment.m:55
        v=size(alpha) / size(theta)
# circ_moment.m:56
        alpha=circ_dist(alpha,repmat(theta,v))
# circ_moment.m:57
    
    
    n=size(alpha,dim)
# circ_moment.m:61
    cbar=sum(multiply(cos(dot(p,alpha)),w),dim) / n
# circ_moment.m:62
    sbar=sum(multiply(sin(dot(p,alpha)),w),dim) / n
# circ_moment.m:63
    mp=cbar + dot(1j,sbar)
# circ_moment.m:64
    rho_p=abs(mp)
# circ_moment.m:66
    mu_p=angle(mp)
# circ_moment.m:67