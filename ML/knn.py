from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV

from data import gendata
import matplotlib.pyplot as plt
import numpy as np
x_train,x_test,y_train,y_test = gendata()

accuracy = []

for n in range(1,11):
    model = KNeighborsClassifier(n_neighbors=n)
    model = model.fit(x_train, y_train)
    accuracy.append(model.score(x_test,y_test))
pram_dict = {'n_neighbors' :np.arange(1,11)}

model = GridSearchCV(KNeighborsClassifier(),param_grid=pram_dict)
model.fit(x_train,y_train)
print(model.best_params_)
plt.plot(np.arange(10),accuracy)




