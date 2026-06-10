import matplotlib.pyplot as plt
import numpy as np

with open('./0409.log', "r", encoding="utf-16") as f:
    lines = f.readlines()
X = []
Y1 =[] #travel costs
Y2 = [] #service cost
Y3 = [] #failure cost
Y4 = [] #total cost
for ix,line in enumerate(lines):
    if 'percentage home delivery:' in line:

        x = line.split(':')[1].strip()
        print(x)
        X.append(float(x))
        Y1.append(float(lines[ix+1].split(':')[1]))
        Y2.append(float(lines[ix+2].split(':')[1]))
        Y3.append(float(lines[ix+3].split(':')[1]))
        Y4.append(float(lines[ix+8].split(':')[1]))

        #
        print(lines[ix+1])
        print(lines[ix+2])
        print(lines[ix+3])
        print(lines[ix+8])


def normalize(X):
    max_x = np.max(X)
    min_x = np.min(X)
    X = (X-min_x)/(max_x-min_x)
    return X

#画图
plt.figure(figsize=(10, 5))
plt.plot(X, normalize(Y1), label='travel costs')
plt.plot(X, normalize(Y2), label='service cost')
plt.plot(X, normalize(Y3), label='failure cost')
# plt.plot(X, Y4, label='total cost')
plt.legend()
plt.xlabel('percentage home delivery')
plt.ylabel('costs')
plt.title('costs')
#plt.savefig('./baseline.png')
plt.show()