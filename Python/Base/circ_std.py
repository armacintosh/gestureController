# Generated with SMOP  0.41
from libsmop import *
# circ_std.m

    
@function
def circ_std(alpha=None,w=None,d=None,dim=None,*args,**kwargs):
    varargin = circ_std.varargin
    nargin = circ_std.nargin

    # s = circ_std(alpha, w, d, dim)
#   Computes circular standard deviation for circular data 
#   (equ. 26.20, Zar).
    
    #   Input:
#     alpha	sample of angles in radians
#     [w		weightings in case of binned angle data]
#     [d    spacing of bin centers for binned data, if supplied 
#           correction factor is used to correct for bias in 
#           estimation of r]
#     [dim  compute along this dimension, default is 1]
    
    #     If dim argument is specified, all other optional arguments can be
#     left empty: circ_std(alpha, [], [], dim)
    
    #   Output:
#     s     angular deviation
#     s0    circular standard deviation
    
    # PHB 6/7/2008
    
    # References:
#   Biostatistical Analysis, J. H. Zar
    
    # Circular Statistics Toolbox for Matlab
    
    # By Philipp Berens, 2009
# berens@tuebingen.mpg.de - www.kyb.mpg.de/~berens/circStat.html
    
    if nargin < 4:
        dim=1
# circ_std.m:32
    
    if nargin < 3 or isempty(d):
        # per default do not apply correct for binned data
        d=0
# circ_std.m:37
    
    if nargin < 2 or isempty(w):
        # if no specific weighting has been specified
  # assume no binning has taken place
        w=ones(size(alpha))
# circ_std.m:43
    else:
        if size(w,2) != size(alpha,2) or size(w,1) != size(alpha,1):
            error('Input dimensions do not match')
    
    # compute mean resultant vector length
    r=circ_r(alpha,w,d,dim)
# circ_std.m:51
    s=sqrt(dot(2,(1 - r)))
# circ_std.m:53
    
    s0=sqrt(dot(- 2,log(r)))
# circ_std.m:54
    