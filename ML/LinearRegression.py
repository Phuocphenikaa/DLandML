from sklearn.linear_model import  LinearRegression
from sklearn.metrics import mean_squared_error,mean_absolute_error
import  numpy as np
import matplotlib.pyplot as plt
from dataLinear import gendata
model = LinearRegression()
x_train,x_test,y_train,y_test = gendata()
model = model.fit(x_train,y_train)
print("Test score:",model.score(x_test,y_test))
print("Train score:",model.score(x_train,y_train))
y_pred = model.predict(x_test)
print("Test mae",mean_absolute_error(y_pred,y_test))

