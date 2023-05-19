import numpy as np
from data import gendata
from batch_generator import batch_gen
class logitic:
    def __init__(self,x,y,lr = 0.0075,epochs = 300,weight_decay = 0.0005):
        self.x = x
        self.y = y
        self.features = x.shape[0]
        self.n = x.shape[1]
        self.w = np.zeros((1,self.features))
        self.bias = np.zeros((1,1))
        self.lr = lr
        self.epochs = epochs
        self.weight_decay = weight_decay
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

        dw = np.mean(np.dot(self.x,dz),axis=1,keepdims=True).T+self.weight_decay*self.w
        db = np.mean(dz)
        assert (self.w.shape==dw.shape)
        return dw,db

    def update(self):
        dw,db = self.grad()
        self.w = self.w -self.lr*dw
        self.bias = self.bias - self.lr*db
    def loss_coumpute(self,y_pred,y):
        esp = 1e-15
        l2 = self.weight_decay*np.sum(pow(self.w,2))
        assert (y.shape==y_pred.shape)
        return -np.mean(np.multiply(y,np.log(y_pred+esp))+np.multiply(1-y,np.log(1-y_pred+esp)))+l2
    def fit(self):
        x = self.x.T
        y = self.y
        for _ in range(self.epochs):
            for batch,(x1,y1) in enumerate(batch_gen(x,y,64)):
                self.x = x1.T
                self.y = y1
                y_pred = model.predict_prob(self.x)
                loss = model.loss_coumpute(y_pred,self.y)
                model.update()
                if(batch%5==0):
                    print(loss)
    def predict(self,x):
        assert (x.shape[0]==self.features)
        y_prob = self.predict_prob(x)
        y_pred = np.where(y_prob>0.5,1,0)
        return y_pred
    def evaluate(self,x,y_test):
        assert (x.shape[0] == self.features and y_test.shape[0]==x.shape[1])
        y_pred = self.predict(x)
        sum_corre = np.sum(np.where(y_test==y_pred,1,0))
        return sum_corre/y_test.shape[0]

x_train,x_test,y_train,y_test = gendata()
x_train = x_train.T
x_test = x_test.T
model = logitic(x_train,y_train)
model.fit()
print(model.predict(x_test))
print()
