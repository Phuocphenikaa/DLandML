from sklearn.tree import DecisionTreeClassifier
from data import gendata
trainx,testx,trainy,testy = gendata()
model = DecisionTreeClassifier()

model = model.fit(trainx,trainy)
print(model.score(testx,testy))