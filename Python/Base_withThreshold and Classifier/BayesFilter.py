# Generated with SMOP  0.41
from libsmop import *
# BayesFilter.m

    
@function
def BayesFilter(emg=None,prior=None,pbins=None,param=None,*args,**kwargs):
    varargin = BayesFilter.varargin
    nargin = BayesFilter.nargin

    ########################################################################
# Improved version of Bayes-Chapman-Kolmogorov filter proposed in      #
# T. Sanger 2007                                                       #
# Author: David Hofmann   -   david.hofmann@mytum.de                   #
# Affiliation: Max Planck Institute for Dynamics and Self-Organization #
########################################################################
# emg:   N dimensional data vector (can be one sample, N = 1).
#        N.B. if N gets too large, numerical problems are encountered when 
#        computing the likelihood!
#        It is suggested to have N no larger than 40.
# prior: histogram distribution. Must be assigned to initial guess (usually
#        flat distribution for first iteration). For all following
#        iterations prior is assigned to the posterior from iteration
#        before.
# pbins: prior bins, values corresponding to the bins of the distribution 
#        of sigma;
#        NOTE: we assume the signals normalized by division with sigmaMVC 
#        -> support of 'sigma' distribution is always between 0 and 1 and 
#        must be multiplied by sigmaMVC to get the actual amplitude estimate
# param: parameter structure containing
#   .alpha:    'diffusion' parameter.
#   .beta:     Master equation transition rate.
#   .sigmaMVC: sigma during maximum voluntary contraction.
#   .sf:       sampling frequency.
#   .model:    defines the likelihood function, either gauss or laplace.
#   .pointmax: 'true' point estimation via maximum, 'false' via expectation value
#   .bins:     number of bins of sigma distribution
    
    # compute time step depending on number of samples in emg and on
    # sampling rate.
    N=length(emg)
# BayesFilter.m:32
    dt=dot(param.sf ** - 1,N)
# BayesFilter.m:33
    dsigma=pbins(2) - pbins(1)
# BayesFilter.m:34
    
    # propagate prior according to time evolution equation
    newPrior=(dot(dot(dt,param.alpha),(concat([[prior(1)],[prior(arange(1,end() - 1))]]) - dot(2,prior) + concat([[prior(arange(2,end()))],[prior(end())]]))) / dsigma ** 2 + dot(dt,param.beta) + dot((1 - dot(dt,param.beta)),prior))
# BayesFilter.m:36
    
    # the grid spacing in the time domain and grid spacing in the state 
    # variable domain sigma must satisfy the following inequality
    # dt < alpha/(2*dsigma^2)
    
    # compute likelihood (assumption of independence => product of
    # likelihoods for each emg sample)
    if 'Gauss' == param.model:
        likelihood=exp(dot(- 0.5,sum(emg ** 2)) / pbins ** 2) / pbins ** N
# BayesFilter.m:48
    else:
        if 'Laplace' == param.model:
            likelihood=exp(- sum(abs(emg)) / pbins) / pbins ** N
# BayesFilter.m:50
        else:
            error('Unknown option for likelihood model')
    
    if pbins(1) == 0:
        likelihood[1]=0
# BayesFilter.m:55
    
    posterior=multiply(likelihood,newPrior)
# BayesFilter.m:58
    posterior=posterior / norm(posterior,1)
# BayesFilter.m:59
    
    # point estimation via maximum or expectation value
    if param.pointmax:
        __,idx=max(posterior,nargout=2)
# BayesFilter.m:62
        map=pbins(idx)
# BayesFilter.m:63
    else:
        map=sum(multiply(posterior,pbins))
# BayesFilter.m:65
    
    return map,posterior
    
if __name__ == '__main__':
    pass
    