import pandas as pd
from  sklearn.model_selection import train_test_split
import numpy as np
data_dir = r"C:\Users\THINKPAD\Downloads\auto-mpg.csv"
def gendata():
    df = pd.read_csv(data_dir)
    df = df.drop(df.loc[df["horsepower"]=="?"].index )
    df = df.iloc[:,:-1]
    df["horsepower"] = df["horsepower"].astype(float)
    X = df.iloc[:, 0:].values
    Y = df.iloc[:, 0].values
    X_min = np.min(X,axis=0,keepdims=True)
    X_max = np.max(X,axis=0,keepdims=True)
    Y_mean = np.mean(Y)
    Y_std = np.std(Y)

    X = (X- X_min)/(X_max-X_min)
    Y = (Y-Y_mean)/(Y_std)

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
    
    return x_train, x_test, y_train, y_test



gendata()