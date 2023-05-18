from sklearn.linear_model import LogisticRegression
from data import gendata
import matplotlib.pyplot as plt
import numpy as np
x_train,x_test,y_train,y_test = gendata()
x_train = x_train[:,0:2]
x_test = x_test[:,0:2]
model = LogisticRegression()
model = model.fit(x_train,y_train)
print("test accuracy ",model.score(x_test,y_test))
print("train accuracy ",model.score(x_train,y_train))
xx_min ,xx_max = x_train[:,0].min(axis = 0,keepdims = True),x_train[:,0].max(axis = 0,keepdims =True)
yy_min ,yy_max = x_train[:,1].min(axis = 0,keepdims = True),x_train[:,1].max(axis =0,keepdims =True)
xx ,yy= np.meshgrid(np.linspace(xx_min,xx_max,100),np.linspace(yy_min,yy_max,100))
x = np.vstack((xx.reshape(-1),yy.reshape(-1))).T
z = model.predict(x).reshape(xx.shape)
plt.scatter(x_train[:,0],x_train[:,1],c = y_train)
plt.contourf(xx,yy,z,alpha = 0.8)
plt.show()

