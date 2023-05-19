import numpy as np
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

# Generate synthetic data
X, y = make_blobs(n_samples=400, n_features=2, centers=2, random_state=8, cluster_std=1.5)
X_min = X.min(axis=0, keepdims=True)
X_max = X.max(axis=0, keepdims=True)
X = (X - X_min) / (X_max - X_min)

# Create meshgrid for contour plot
a, b = np.mgrid[0:1:0.01, 0:1:0.01]
pos = np.dstack((a, b))

# Fit Gaussian distributions to each class
X1 = X[y == 0, :]
mu1 = X1.mean(axis=0)
sigma1 = np.cov(X1.T)
g1 = multivariate_normal(mu1, sigma1)

X2 = X[y == 1, :]
mu2 = X2.mean(axis=0)
sigma2 = np.cov(X2.T)
g2 = multivariate_normal(mu2, sigma2)

# Plot the data points and decision boundaries
plt.figure()

# Plot the contours for class 0
plt.contourf(a, b, g1.pdf(pos), cmap='Reds', alpha=0.5)

# Plot the contours for class 1
plt.contourf(a, b, g2.pdf(pos), cmap='Greens', alpha=0.3)

# Scatter plot of data points
plt.scatter(X[y == 0, 0], X[y == 0, 1], c='r', label='Class 0')
plt.scatter(X[y == 1, 0], X[y == 1, 1], c='g', label='Class 1')

plt.legend()
plt.show()
