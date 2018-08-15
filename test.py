from vpython import *
import math
a = vector(0.71,-0.5,0.5)
b = vector(1.42,-0.71,-0.71)
print(math.isclose(a.dot(b), 1, rel_tol=1e-2))
