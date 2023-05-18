import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

# Fetch the dataset from the original source
data_url = "http://lib.stat.cmu.edu/datasets/boston"
raw_df = pd.read_csv(data_url, sep="\s+", skiprows=22, header=None)
data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
target = raw_df.values[1::2, 2]

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=42)

# 1. Linear Regression
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Evaluate Linear Regression model on the test set
y_pred_lr = lr_model.predict(X_test)
r2_lr = r2_score(y_test, y_pred_lr)
rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))
mae_lr = mean_absolute_error(y_test, y_pred_lr)

print("Linear Regression:")
print("R2 Score:", r2_lr)
print("RMSE:", rmse_lr)
print("MAE:", mae_lr)

# 2. Ridge Regression with GridSearchCV
ridge_model = Ridge()
params = {'alpha': [0.001, 0.01, 0.1, 1.0, 10.0]}
ridge_cv = GridSearchCV(ridge_model, params)
ridge_cv.fit(X_train, y_train)

# Find the best alpha for Ridge Regression
best_alpha = ridge_cv.best_params_['alpha']

# Build Ridge Regression model with the best alpha
ridge_model_best = Ridge(alpha=best_alpha)
ridge_model_best.fit(X_train, y_train)

# Evaluate Ridge Regression model on the test set
y_pred_ridge = ridge_model_best.predict(X_test)
r2_ridge = r2_score(y_test, y_pred_ridge)
rmse_ridge = np.sqrt(mean_squared_error(y_test, y_pred_ridge))
mae_ridge = mean_absolute_error(y_test, y_pred_ridge)

print("\nRidge Regression (Best Alpha = {}):".format(best_alpha))
print("R2 Score:", r2_ridge)
print("RMSE:", rmse_ridge)
print("MAE:", mae_ridge)

# 3. Graph alpha-dependent coefficients for Ridge Regression
alphas = np.logspace(-3, 3, num=100)
coefs = []
for alpha in alphas:
    ridge_model = Ridge(alpha=alpha)
    ridge_model.fit(X_train, y_train)
    coefs.append(ridge_model.coef_)

# Plotting alpha-dependent coefficients
plt.figure(figsize=(10, 6))
plt.plot(alphas, coefs)
plt.xscale('log')
plt.xlabel('Alpha')
plt.ylabel('Coefficients')
plt.title('Ridge Regression: Alpha-dependent Coefficients')
plt.legend(raw_df.columns[:-1])
plt.show()



