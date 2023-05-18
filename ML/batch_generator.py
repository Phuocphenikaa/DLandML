import math
def batch_gen(x,y,batch_size = 64):
    batch_num = math.ceil(x.shape[0]/batch_size)
    for i in range(batch_num-1):
        x_batch = x[i*batch_size:(i+1)*batch_size,:]
        y_batch = y[i*batch_size:(i+1)*batch_size]
        yield x_batch,y_batch
    yield x[(batch_num-1)*batch_size:,:],y[(batch_num-1)*batch_size:]

