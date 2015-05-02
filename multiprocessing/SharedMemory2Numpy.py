import multiprocessing
import numpy as np
import ctypes

class shared2np:
	def __init__(self):
		self._ctypes_to_numpy = {
			ctypes.c_char : np.int8,
			ctypes.c_wchar : np.int16,
			ctypes.c_byte : np.int8,
			ctypes.c_ubyte : np.uint8,
			ctypes.c_short : np.int16,
			ctypes.c_ushort : np.uint16,
			ctypes.c_int : np.int32,
			ctypes.c_uint : np.int32,
			ctypes.c_long : np.int32,
			ctypes.c_ulong : np.int32,
			ctypes.c_float : np.float32,
			ctypes.c_double : np.float64
			}

	def shmem_as_ndarray(self,array_or_value):
		"""view processing.Array or processing.Value as ndarray"""
		obj = array_or_value.get_obj()
		t = self._ctypes_to_numpy[obj._type_]
		print t
		return np.frombuffer(obj,dtype=t)

## Test it out
#a = multiprocessing.Array(ctypes.c_double,10*10)
#s2np = shared2np()
#anp = s2np.shmem_as_ndarray(a)
#anpre = anp.reshape((10,10))
#print anp
#print anpre
