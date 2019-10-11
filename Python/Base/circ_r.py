# Generated with SMOP  0.41
from libsmop import *
# circ_r.m

    
@function
def circ_r(alpha=None,w=None,d=None,dim=None,*args,**kwargs):
    varargin = circ_r.varargin
    nargin = circ_r.nargin

    # r = circ_r(alpha, w, d)
#   Computes mean resultant vector length for circular data.
    
    #   Input:
#     alpha	sample of angles in radians
#     [w		number of incidences in case of binned angle data]
#     [d    spacing of bin centers for binned data, if supplied 
#           correction factor is used to correct for bias in 
#           estimation of r, in radians (!)]
#     [dim  compute along this dimension, default is 1]
    
    #     If dim argument is specified, all other optional arguments can be
#     left empty: circ_r(alpha, [], [], dim)
    
    #   Output:
#     r		mean resultant length
    
    # PHB 7/6/2008
    
    # References:
#   Statistical analysis of circular data, N.I. Fisher
#   Topics in circular statistics, S.R. Jammalamadaka et al. 
#   Biostatistical Analysis, J. H. Zar
    
    # Circular Statistics Toolbox for Matlab
    
    # By Philipp Berens, 2009
# berens@tuebingen.mpg.de - www.kyb.mpg.de/~berens/circStat.html
    
    if nargin < 4:
        dim=1
# circ_r.m:32
    
    if nargin < 2 or isempty(w):
        # if no specific weighting has been specified
  # assume no binning has taken place
        w=ones(size(alpha))
# circ_r.m:38
    else:
        if size(w,2) != size(alpha,2) or size(w,1) != size(alpha,1):
            error('Input dimensions do not match')
    
    if nargin < 3 or isempty(d):
        # per default do not apply correct for binned data
        d=0
# circ_r.m:47
    
    # compute weighted sum of cos and sin of angles
    r=sum(multiply(w,exp(dot(1j,alpha))),dim)
# circ_r.m:51
    # obtain length
    r=abs(r) / sum(w,dim)
# circ_r.m:54
    # for data with known spacing, apply correction factor to correct for bias
# in the estimation of r (see Zar, p. 601, equ. 26.16)
    if d != 0:
        c=d / 2 / sin(d / 2)
# circ_r.m:59
        r=dot(c,r)
# circ_r.m:60
    