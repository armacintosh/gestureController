# Generated with SMOP  0.41
from libsmop import *
# circ_confmean.m

    
@function
def circ_confmean(alpha=None,xi=None,w=None,d=None,dim=None,*args,**kwargs):
    varargin = circ_confmean.varargin
    nargin = circ_confmean.nargin

    
    # t = circ_mean(alpha, xi, w, d, dim)
#   Computes the confidence limits on the mean for circular data.
    
    #   Input:
#     alpha	sample of angles in radians
#     [xi   (1-xi)-confidence limits are computed, default 0.05]
#     [w		number of incidences in case of binned angle data]
#     [d    spacing of bin centers for binned data, if supplied 
#           correction factor is used to correct for bias in 
#           estimation of r, in radians (!)]
#     [dim  compute along this dimension, default is 1]
    
    #   Output:
#     t     mean +- d yields upper/lower (1-xi)# confidence limit
    
    # PHB 7/6/2008
    
    # References:
#   Statistical analysis of circular data, N. I. Fisher
#   Topics in circular statistics, S. R. Jammalamadaka et al. 
#   Biostatistical Analysis, J. H. Zar
    
    # Circular Statistics Toolbox for Matlab
    
    # By Philipp Berens, 2009
# berens@tuebingen.mpg.de - www.kyb.mpg.de/~berens/circStat.html
    
    if nargin < 5:
        dim=1
# circ_confmean.m:31
    
    if nargin < 4 or isempty(d):
        # per default do not apply correct for binned data
        d=0
# circ_confmean.m:36
    
    if nargin < 3 or isempty(w):
        # if no specific weighting has been specified
  # assume no binning has taken place
        w=ones(size(alpha))
# circ_confmean.m:42
    else:
        if size(w,2) != size(alpha,2) or size(w,1) != size(alpha,1):
            error('Input dimensions do not match')
    
    # set confidence limit size to default
    if nargin < 2 or isempty(xi):
        xi=0.05
# circ_confmean.m:51
    
    # compute ingredients for conf. lim.
    r=circ_r(alpha,w,d,dim)
# circ_confmean.m:55
    n=sum(w,dim)
# circ_confmean.m:56
    R=multiply(n,r)
# circ_confmean.m:57
    c2=chi2inv((1 - xi),1)
# circ_confmean.m:58
    # check for resultant vector length and select appropriate formula
    t=zeros(size(r))
# circ_confmean.m:61
    for i in arange(1,numel(r)).reshape(-1):
        if r(i) < 0.9 and r(i) > sqrt(c2 / 2 / n(i)):
            t[i]=sqrt((dot(dot(2,n(i)),(dot(2,R(i) ** 2) - dot(n(i),c2)))) / (dot(4,n(i)) - c2))
# circ_confmean.m:65
        else:
            if r(i) >= 0.9:
                t[i]=sqrt(n(i) ** 2 - dot((n(i) ** 2 - R(i) ** 2),exp(c2 / n(i))))
# circ_confmean.m:67
            else:
                t[i]=NaN
# circ_confmean.m:69
                warning('Requirements for confidence levels not met.')
    
    # apply final transform
    t=acos(t / R)
# circ_confmean.m:75