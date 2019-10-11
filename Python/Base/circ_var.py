# Generated with SMOP  0.41
from libsmop import *
# circ_var.m

    
@function
def circ_var(alpha=None,w=None,d=None,dim=None,*args,**kwargs):
    varargin = circ_var.varargin
    nargin = circ_var.nargin

    # s = circ_var(alpha, w, d, dim)
#   Computes circular variance for circular data 
#   (equ. 26.17/18, Zar).
    
    #   Input:
#     alpha	sample of angles in radians
#     [w		number of incidences in case of binned angle data]
#     [d    spacing of bin centers for binned data, if supplied 
#           correction factor is used to correct for bias in 
#           estimation of r]
#     [dim  compute along this dimension, default is 1]
    
    #     If dim argument is specified, all other optional arguments can be
#     left empty: circ_var(alpha, [], [], dim)
    
    #   Output:
#     S     circular variance 1-r
#     s     angular variance 2*(1-r)
    
    # PHB 6/7/2008
    
    # References:
#   Statistical analysis of circular data, N.I. Fisher
#   Topics in circular statistics, S.R. Jammalamadaka et al. 
#   Biostatistical Analysis, J. H. Zar
    
    # Circular Statistics Toolbox for Matlab
    
    # By Philipp Berens, 2009
# berens@tuebingen.mpg.de - www.kyb.mpg.de/~berens/circStat.html
    
    if nargin < 4:
        dim=1
# circ_var.m:34
    
    if nargin < 3 or isempty(d):
        # per default do not apply correct for binned data
        d=0
# circ_var.m:39
    
    if nargin < 2 or isempty(w):
        # if no specific weighting has been specified
  # assume no binning has taken place
        w=ones(size(alpha))
# circ_var.m:45
    else:
        if size(w,2) != size(alpha,2) or size(w,1) != size(alpha,1):
            error('Input dimensions do not match')
    
    # compute mean resultant vector length
    r=circ_r(alpha,w,d,dim)
# circ_var.m:53
    # apply transformation to var
    S=1 - r
# circ_var.m:56
    s=dot(2,S)
# circ_var.m:57