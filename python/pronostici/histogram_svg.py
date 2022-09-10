import matplotlib.pyplot as plt
import numpy as np
import io

f = io.BytesIO()
a = np.random.rand(10)
plt.bar(range(len(a)), a)
plt.savefig(f, format = "svg")

print(f.getvalue()) # svg string
