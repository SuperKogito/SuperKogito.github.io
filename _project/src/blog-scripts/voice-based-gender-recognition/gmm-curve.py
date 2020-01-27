import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture

# format style 
plt.rcParams['axes.grid']  = True
plt.rcParams['grid.color'] = 'w'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.linewidth'] = .2
plt.rcParams['axes.edgecolor']  = '#1171A2'
plt.rcParams['axes.facecolor']  = '#1d1f21'
plt.rcParams['axes.labelcolor'] = '#1171A2'
plt.rcParams['boxplot.capprops.color'] = '#1d1f21'
plt.rcParams['boxplot.flierprops.markeredgecolor'] = '#1d1f21'
plt.rcParams['boxplot.meanprops.color'] = '#1d1f21'
plt.rcParams['boxplot.meanprops.markeredgecolor'] = '#1d1f21'
plt.rcParams['boxplot.meanprops.markerfacecolor'] = '#1d1f21'
plt.rcParams['boxplot.whiskerprops.color'] = '#1d1f21'
plt.rcParams['figure.edgecolor'] = '#1d1f21'
plt.rcParams['figure.facecolor'] = '#1d1f21'
plt.rcParams['grid.color'] = '#1d1f21'
plt.rcParams['lines.color'] = '#1d1f21'
plt.rcParams['patch.edgecolor'] = '#1d1f21'
plt.rcParams['patch.facecolor'] = '#1d1f21'
plt.rcParams['savefig.edgecolor'] = '#1d1f21'
plt.rcParams['savefig.facecolor'] = '#1d1f21'
plt.rcParams['text.color'] = '#1171A2'
plt.rcParams['xtick.color'] = '#1171A2'
plt.rcParams['ytick.color'] = '#1171A2'

# init colors 
colors = ['yellow', 'red','green', 'blue']


def plot_distribution(samples, i, label, n):
    #ax.hist(samples, bins=30, normed=True, alpha=0.5, color="#0070FF")
    # Fit GMM
    gmm = GaussianMixture(n_components=n, covariance_type="full", tol=0.001)
    gmm = gmm.fit(X=np.expand_dims(samples, 1))
    # Evaluate GMM
    gmm_x = np.linspace(-2, 1.5, len(samples))
    gmm_y = np.exp(gmm.score_samples(gmm_x.reshape(-1, 1)))
    if i == 3 : gmm_y = gmm_y * 2.159 - .005
    if i == 0 : gmm_y = gmm_y * .7
    if i == 1 : gmm_y = gmm_y * .7
    if i == 2 : gmm_y = gmm_y * .7

    if n == 3: ax.plot(gmm_x, gmm_y, color=colors[i], ls="--", lw=4, label=label)    
    else     : ax.plot(gmm_x, gmm_y, color=colors[i], ls="-",  lw=4, label=label)    

# Generate sample from three gaussian distributions
samples1 = np.random.normal(-0.75, 0.215, 1000)
samples2 = np.random.normal( 0.00, 0.145, 1000)
samples3 = np.random.normal( 0.75, 0.215, 1000)

samplesx  = np.array(list(samples1) + list(samples2) + list(samples3))
# Make regular histogram
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[10, 8], facecolor=(.29,.31,.33))
plot_distribution(samples1, 0,'Gaussian density of 1st samples', 1)
plot_distribution(samples2, 1,'Gaussian density of 2nd samples', 1)
plot_distribution(samples3, 2,'Gaussian density of 3rd samples', 1)
plot_distribution(samplesx, 3,'Gaussian Mixture model of all samples', 3)


# Annotate diagram
ax.set_ylabel("Probability density")
ax.set_xlabel("Arbitrary units")
ax.grid(False)
    
# Draw legend
plt.rcParams['patch.edgecolor'] = "red"

ax.legend(shadow=False, framealpha=0.0, facecolor=None)
plt.show()
fig.savefig("../../../docs/source/_static/blog-plots/voice-based-gender-recognition/gmm.png",  transparent=True)


##!/usr/bin/env python
#import psutil
#print("Duration:", time.time() - t)
## gives a single float value
#print("cpu:", psutil.cpu_percent())
## gives an object with many fields
#print("virtual memory", psutil.virtual_memory())
## you can convert that object to a dictionary 
#print(dict(psutil.virtual_memory()._asdict()))