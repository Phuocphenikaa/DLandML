import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from tqdm import tqdm
class KMean:
  def __init__(self,k = 2):
    if(k<2):
      print("K cluster must gt 2")
      return
    self.k = k
  def fit(self,x,y,x_vali,y_valid,num_iter = 200,patient = 8):
    model = None
    self.cluster = []
    self.categori = []
    count_imp = 0
    imp_check = 1
    for i in range(self.k):
      self.categori.append({})

    self.cluster = [np.random.random((x.shape[1],)) for _ in range(self.k)]  # Initialize cluster centroids
    best_accuracy = 0
    for _ in tqdm(range(num_iter)):
      if imp_check==0:
        break
      for i in range(x.shape[0]):
        xi = x[i,:]
        index_cluster_closest = self.findClosest(xi)
        for index_cluster in range(self.k):
          if i in self.categori[index_cluster]:
            self.categori[index_cluster].pop(i)
            break
        self.categori[index_cluster_closest][i] = xi
        self.updateCluster(index_cluster_closest)
      if _ % 10 == 0:
        valid_accuracy = self.evaluate(x_vali,y_valid)
        if valid_accuracy>best_accuracy:
          best_accuracy = valid_accuracy
          count_imp = 0
          model = self
        else:
          count_imp+=1
          if count_imp > patient:
            imp_check = 0
    while(self.swap(x,y)):
      pass
    return model
  def predict(self,x):
    assert (len(x.shape)==2)
    y = []
    for i in range(x.shape[0]):
      xi = x[i,:]

      y.append(self.findClosest(xi))
    return y

  def predict2(self, x):
    assert (len(x.shape) == 2)
    y = []
    for i in range(x.shape[0]):
      xi = x[i, :]

      y.append(self.findClosest2(xi))
    return y
  def evaluate(self,x,y):
    y_pred = np.array(self.predict(x))
    y = np.array(y)
    return np.sum(np.where(y==y_pred,1,0))/y.shape[0]

  def swap(self,x,y):
    accuracy_old = self.evaluate(x,y)
    for i in range(self.k):
      temp_clu = self.cluster[i]
      temp_cate = self.categori[i]
      for j in range(self.k):
        if i == j:
          continue
        self.cluster[i] = self.cluster[j]
        self.categori[i] = self.categori[j]
        self.categori[j] = temp_cate
        self.cluster[j] = temp_clu

        accuracy_new = self.evaluate(x,y)
        if accuracy_old<accuracy_new:
          print("impove")
          return True
        else:
          self.categori[j] = self.categori[i]
          self.cluster[j] = self.cluster[i]
          self.cluster[i] = temp_clu
          self.categori[i] = temp_cate

    return False

  def updateCluster(self,index):
    value = self.categori[index].values()
    value = np.array(list(value))
    value = np.squeeze(value.mean(axis=0,keepdims=True))
    self.cluster[index] = value
  def ecuDistance(self,x1,x2):
      return np.sqrt(np.sum(pow(np.abs(x1-x2),2)))
  def findClosest(self,x):
    min = 99999
    count = 0
    min_index = 0
    assert (len(x.shape)==1)
    for cluster in self.cluster:
      distance = self.ecuDistance(cluster,x)
      if distance<min:
        min = distance
        min_index = count
      count += 1
    return min_index
  def findClosest2(self,x):
    min = 99999
    count = 0
    min_index = 0
    assert (len(x.shape)==1)
    for cluster in self.cluster:
      distance = self.ecuDistance(cluster[0:2],x)
      if distance<min:
        min = distance
        min_index = count
      count += 1
    return min_index









#
# x = np.random.randint(1,200,size = (10,3))
# y = np.random.randint(0,2,size = (10,))
# b = np.random.randint(0,10,size = (2))
centers=4
model = KMean(k = centers)
X, y = make_blobs(cluster_std=2,n_samples=700, n_features=10, centers=centers)
X,x_test,y,y_test = train_test_split(X,y,random_state=8,test_size=0.3)
x_test,x_valid,y_test,y_valid = train_test_split(x_test,y_test,test_size=0.5)
model.fit(X,y,x_valid,y_valid)
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1), np.arange(y_min, y_max, 0.1))

# Use the model to predict the class labels for each point on the grid
Z = np.array(model.predict2(np.c_[xx.ravel(), yy.ravel()]))

Z = Z.reshape(xx.shape)

# Plot the decision boundary
plt.contourf(xx, yy, Z, alpha=0.8)
plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Decision Boundary')
plt.show()
print(model.evaluate(x_test,y_test))
