from sklearn.linear_model import LogisticRegression
from data import gendata
x_train,x_test,y_train,y_test = gendata()
model = LogisticRegression()
model = model.fit(x_train,y_train)
print("test accuracy ",model.score(x_test,y_test))
print("train accuracy ",model.score(x_train,y_train))
