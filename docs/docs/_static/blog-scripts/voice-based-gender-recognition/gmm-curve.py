import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture

"""
def style_plt(ax):
    sns.set(style='ticks', palette='Set2')
    #plt.style.use("grayscale")
    #plt.style.use('ggplot')
    plt.rcParams['text.usetex'] = True
    plt.rcParams.update({'font.size': 16})
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica"]})
    
    ax.tick_params(axis = 'both', which = 'major', labelsize = 16)
    ax.tick_params(axis = 'both', which = 'minor', labelsize = 16)    

def gmm_xy(samples, n):
    # Fit GMM
    gmm = GaussianMixture(n_components=n, covariance_type="full", tol=0.001)
    gmm = gmm.fit(X=np.expand_dims(samples, 1))
    # Evaluate GMM
    gmm_x = np.linspace(-1.5, 1.5, len(samples))
    gmm_y = np.exp(gmm.score_samples(gmm_x.reshape(-1, 1)))
    return gmm_x, gmm_y
    

# Generate sample from three gaussian distributions
samples1 = np.random.normal(-0.5, 0.25, 1000)
samples2 = np.random.normal( 0.0, 0.15, 1000)
samples3 = np.random.normal( 0.5, 0.20, 1000)

# get gmms data 
gmmx1, gmmy1 = gmm_xy(samples1, 1)
gmmx2, gmmy2 = gmm_xy(samples2, 1)
gmmx3, gmmy3 = gmm_xy(samples3, 1)

gmmy = np.array([max(gmmy1[i], gmmy2[i], gmmy3[i]) for i in range(len(gmmy1))])

# Make regular histogram
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[10, 10], facecolor=(.29,.31,.33))
style_plt(ax)

ax.plot(gmmx1, gmmy1, ls="-", lw=2, label='Gaussian density of 1st batch of samples')
ax.plot(gmmx2, gmmy2, ls="-", lw=2, label='Gaussian density of 2nd batch of samples')
ax.plot(gmmx3, gmmy3, ls="-", lw=2, label='Gaussian density of 3rd batch of samples')
ax.plot(gmmx1, gmmy, ls="--", lw=4, label='Gaussian Mixture model of all samples')

# Annotate diagram
ax.set_ylabel("Probability density")
ax.set_xlabel("Arbitrary units")
ax.grid(False)
    
ax.legend(shadow=False, framealpha=0.0, facecolor=None)
plt.show()

fig.tight_layout()
fig.savefig("../../../_static/blog-plots/voice-based-gender-recognition/gmm.png",  
            transparent=True)


##!/usr/bin/env python
#import psutil
#print("Duration:", time.time() - t)
## gives a single float value
#print("cpu:", psutil.cpu_percent())
## gives an object with many fields
#print("virtual memory", psutil.virtual_memory())
## you can convert that object to a dictionary 
#print(dict(psutil.virtual_memory()._asdict()))

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from mpl_toolkits.mplot3d import Axes3D
from sklearn import mixture

def bivariate_normal(X, Y, sigmax=1.0, sigmay=1.0,
                 mux=0.0, muy=0.0, sigmaxy=0.0):
    """
    Bivariate Gaussian distribution for equal shape *X*, *Y*.
    See `bivariate normal
    <http://mathworld.wolfram.com/BivariateNormalDistribution.html>`_
    at mathworld.
    """
    Xmu = X-mux
    Ymu = Y-muy

    rho = sigmaxy/(sigmax*sigmay)
    z = Xmu**2/sigmax**2 + Ymu**2/sigmay**2 - 2*rho*Xmu*Ymu/(sigmax*sigmay)
    denom = 2*np.pi*sigmax*sigmay*np.sqrt(1-rho**2)
    return np.exp(-z/(2*(1-rho**2))) / denom

def q(x, y):
	g1 = bivariate_normal(x, y, 1.0, 1.0, -1, -1, -0.8)
	g2 = bivariate_normal(x, y, 1.5, 0.8, 1, 2, 0.6)
	return 0.6*g1+28.4*g2/(0.6+28.4)

def plot_q():
	fig = plt.figure(figsize=(12, 12))
	ax = fig.gca(projection='3d')
	X = np.arange(-5, 5, 0.1)
	Y = np.arange(-5, 5, 0.1)
	X, Y = np.meshgrid(X, Y)
	Z = q(X, Y)
	surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('coolwarm'),
			linewidth=0, antialiased=True)
	fig.colorbar(surf, shrink=0.5, aspect=5)

	plt.savefig('3dgauss.png')
	plt.clf()

def sample():
	'''Metropolis Hastings'''
	N = 10000
	s = 10
	r = np.zeros(2)
	p = q(r[0], r[1])
	print(p)
	samples = []
	for i in range(N):
		rn = r + np.random.normal(size=2)
		pn = q(rn[0], rn[1])
		if pn >= p:
			p = pn
			r = rn
		else:
			u = np.random.rand()
			if u <= pn/p:
				p = pn
				r = rn
		if i % s == 0:
			samples.append(r)

	samples = np.array(samples)
	plt.scatter(samples[:, 0], samples[:, 1], alpha=0.5, s=1)

	'''Plot target'''
	dx = 0.01
	x = np.arange(np.min(samples), np.max(samples), dx)
	y = np.arange(np.min(samples), np.max(samples), dx)
	X, Y = np.meshgrid(x, y)
	Z = q(X, Y)
	CS = plt.contour(X, Y, Z, 10, alpha=0.5)
	plt.clabel(CS, inline=1, fontsize=10)
	plt.savefig("samples.png")
	return samples

def fit_samples(samples):
	gmix = GaussianMixture(n_components=2, covariance_type='full')
	gmix.fit(samples)
	print(gmix.means_)
	colors = ['r' if i==0 else 'g' for i in gmix.predict(samples)]
	ax = plt.gca()
	ax.scatter(samples[:,0], samples[:,1], c=colors, alpha=0.8)
	plt.savefig("class.png")

plot_q()
s = sample()
fit_samples(s)
