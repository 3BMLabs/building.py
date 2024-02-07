import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from objects.panel import *
from objects.frame import *
from objects.steelshape import *
from exchange.speckle import *
from library.profile import data as jsondata
from library.material import *
from library.profile import profiledataToShape
from objects.annotation import *
from abstract.intersect2d import *
from geometry.systemsimple import *
from objects.shape import *
from sandbox_dev.Workspace.WorkEnvObject import *

# # import module
# import numpy as np

# # explicit function to normalize array
# def normalize(arr):
# 	norm_arr = []
# 	diff_arr = max(arr) - min(arr)
# 	for i in arr:
# 		temp = (((i - min(arr))*1)/diff_arr) + 0
# 		norm_arr.append(temp)
# 	return norm_arr

# # assign array and range
# array_1d = [1, 2, 4, 8, 10, 15]
# range_to_normalize = (0, 1)
# normalized_array_1d = normalize(array_1d)

# # display original and normalized array
# print("Original Array = ", array_1d)
# print("Normalized Array = ", normalized_array_1d)


i = [0,0,0]

#new function
import numpy as np

def normalize(v1, axis=-1, order=2):
    v1 = Vector3.to_matrix(v1)
    l2 = np.atleast_1d(np.linalg.norm(v1, order, axis))
    l2[l2==0] = 1
    i = v1 / np.expand_dims(l2, axis)[0]
    return Vector3(i[0],i[1],i[2])

print(Vector3.normalize(Vector3(i[0],i[1],i[2])))

#old function
# def normalize(v1):
#     length = Vector3.length(v1)
#     scale = 1 / length

#     return Vector3(v1.x * scale, v1.y * scale, v1.z * scale)

# print(normalize(Vector3(i[0],i[1],i[2])))