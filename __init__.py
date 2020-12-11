import numpy as np
from .utils import loadXsection, buildInterpolator

_interpolators = []
for i in range(1, 101):
    filename = "%02d.txt" % i
    E_phot, atten = loadXsection(filename)
    interp = buildInterpolator(E_phot, atten)
    _interpolators.append(interp)

def getMassAtten(E, Z):
    """Returns the mass attenuation coefficient (cm^2/g) of
    atomic number Z at energy E (in MeV)"""
    if Z < 1 or Z > 100:
        raise ValueError("Z must be between 1 and 100")
    elif np.min(E) < 1e-3 or np.max(E) > 1e5:
        raise ValueError("Energy must be between 1 keV and 100 GeV")
    idx1 = np.floor(Z-1).astype('int')
    idx2 = np.ceil(Z-1).astype('int')
    atten1 = _interpolators[idx1](E)
    if idx1 == idx2:
        return atten1
    else:
        print("Non-integer Z inputted, interpolating between Z = %d and Z = %d"
              % (np.floor(Z), np.ceil(Z)))
        atten2 = _interpolators[idx2](E)
        f = Z % 1
        return f * atten2 + (1 - f) * atten1
