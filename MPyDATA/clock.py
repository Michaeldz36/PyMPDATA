import numba
import ctypes
import platform

if platform.system() == 'Windows':
    from ctypes.util import find_msvcrt
    lib = find_msvcrt()
    if lib is None:
        lib = 'msvcrt.dll'
else:
    from ctypes.util import find_library
    lib = find_library('c')

clock = ctypes.CDLL(lib).clock
clock.argtypes = []

scale = 1
if platform.system() == 'Linux':
    scale = 1000


@numba.njit()
def time():
    value = clock()
    return value // scale
