# Generated with SMOP  0.41
from libsmop import *
# circ_dist.m

    
@function
def circ_dist(x=None,y=None,*args,**kwargs):
    varargin = circ_dist.varargin
    nargin = circ_dist.nargin

    
    # r = circ_dist(alpha, beta)
#   Pairwise difference x_i-y_i around the circle computed efficiently.
    
    #   Input:
#     alpha      sample of linear random variable
#     beta       sample of linear random variable or one single angle
    
    #   Output:
#     r       matrix with differences
    
    # References:
#     Biostatistical Analysis, J. H. Zar, p. 651
    
    # PHB 3/19/2009
    
    # Circular Statistics Toolbox for Matlab
    
    # By Philipp Berens, 2009
# berens@tuebingen.mpg.de - www.kyb.mpg.de/~berens/circStat.html
    
    if size(x,1) != size(y,1) and size(x,2) != size(y,2) and length(y) != 1:
        error('Input dimensions do not match.')
    
    r=angle(exp(dot(1j,x)) / exp(dot(1j,y)))
# circ_dist.m:28