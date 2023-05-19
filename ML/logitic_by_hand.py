import numpy as np
from data import gendata
class logitic:
    def __init__(self,x,y,lr = 0.0075,epochs = 200):
        self.x = x
        self.y = y
        self.features = x.shape[0]
        self.n = x.shape[1]
        self.w = np.zeros((1,self.features))
        self.bias = np.zeros((1,1))
        self.lr = lr
        self.epochs = epochs
    def sigmoid(self,x):
        return 1/(1+np.exp(-x))
    def predict_prob(self,x):
        assert (x.shape[0]==self.features)
        y_pred = np.dot(self.w,self.x)+self.bias
        y_pred = self.sigmoid(y_pred)
        y_pred = y_pred.reshape(-1,)
        return y_pred
    def grad(self):
        y_pred = self.predict_prob(self.x)
        dz = y_pred-self.y
        dz = dz.reshape(-1,1)
        dw = np.mean(np.dot(self.x,dz),axis=1,keepdims=True).T
        db = np.mean(dz)
        assert (self.w.shape==dw.shape)
        return dw,db
    def update(self):
        dw,db = self.grad()
        self.w = self.w -self.lr*dw
        self.bias = self.bias - self.lr*db
    def loss_coumpute(self,y_pred,y):
        esp = 1e-15
        assert (y.shape==y_pred.shape)
        return -np.mean(np.multiply(y,np.log(y_pred+esp))+np.multiply(1-y,np.log(1-y_pred+esp)))
    def fit(self):
        for _ in range(self.epochs):
            y_pred = model.predict_prob(self.x)
            loss = model.loss_coumpute(y_pred,self.y)
            model.update()
            print(loss)

x_train,x_test,y_train,y_test = gendata()
x_train = x_train.T
x_test = x_test.T
model = logitic(x_train,y_train)
model.fit()
