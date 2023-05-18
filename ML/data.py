import pandas as pd
from sklearn.model_selection import train_test_split
data_dir  = r"C:\Users\THINKPAD\Downloads\Social_Network_Ads-1.csv"
df = pd.read_csv(data_dir)
def gendata():
    df.loc[df['Gender']=="Male","Gender"] = 1
    df.loc[df['Gender'] == "Female","Gender"] = 0
    df['Gender'] = df['Gender'].astype(int)
    X = df.iloc[:,:-1].values
    X = (X-X.min(axis = 0,keepdims =True))/(X.max(axis = 0,keepdims =True)-X.min(axis = 0,keepdims =True))
    Y = df.iloc[:,-1].values
    x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size=0.2)
    return x_train,x_test,y_train,y_test
