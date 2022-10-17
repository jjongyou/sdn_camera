import numpy as np

# x = np.array([[0, 1], [2, 3]], dtype='<u2')
x = np.array([[0, 1], [2, 3]])
print(x.tobytes())
print(type(x.tobytes()))
print(len(x.tobytes()))
