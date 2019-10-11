# Generated with SMOP  0.41
from libsmop import *
# circ_mean.m

    
@function
def circ_mean(alpha=None,w=None,dim=None,*args,**kwargs):
    varargin = circ_mean.varargin
    nargin = circ_mean.nargin

    
    # mu = circ_mean(alpha, w)
#   Computes the mean direction for circular data.
    
    #   Input:
#     alpha	sample of angles in radians
#     [w		weightings in case of binned angle data]
#     [dim  compute along this dimension, default is 1]
    
    #     If dim argument is specified, all other optional arguments can be
#     left empty: circ_mean(alpha, [], dim)
    
    #   Output:
#     mu		mean direction
#     ul    upper 95# confidence limit
#     ll    lower 95# confidence limit
    
    # PHB 7/6/2008
    
    # References:
#   Statistical analysis of circular data, N. I. Fisher
#   Topics in circular statistics, S. R. Jammalamadaka et al. 
#   Biostatistical Analysis, J. H. Zar
    
    # Circular Statistics Toolbox for Matlab
    
    # By Philipp Berens, 2009
# berens@tuebingen.mpg.de - www.kyb.mpg.de/~berens/circStat.html
    
    if nargin < 3:
        dim=1
# circ_mean.m:32
    
    if nargin < 2 or isempty(w):
        # if no specific weighting has been specified
  # assume no binning has taken place
        w=ones(size(alpha))
# circ_mean.m:38
    else:
        if size(w,2) != size(alpha,2) or size(w,1) != size(alpha,1):
            error('Input dimensions do not match')
    
    # compute weighted sum of cos and sin of angles
    r=sum(multiply(w,exp(dot(1j,alpha))),dim)
# circ_mean.m:46
    # obtain mean by
    mu=angle(r)
# circ_mean.m:49
    # AM ADDED - converts negative to + circ means...
    if mu < 0:
        mu=mu + dot(2,pi)
# circ_mean.m:53
    
    # confidence limits if desired
    if nargout > 1:
        t=circ_confmean(alpha,0.05,w,[],dim)
# circ_mean.m:58
        ul=mu + t
# circ_mean.m:59
        ll=mu - t
# circ_mean.m:60
    