import numpy as np
from .utils import loadXsection, buildInterpolator

_atten_interpolators = []
_absorp_interpolators = []
for Z in range(1, 93):
    filename = "%02d.txt" % Z
    E_phot, atten, absorp = loadXsection(filename)
    atten_interp = buildInterpolator(E_phot, atten)
    absorp_interp = buildInterpolator(E_phot, absorp)
    _atten_interpolators.append(atten_interp)
    _absorp_interpolators.append(absorp_interp)
    
del Z, filename, E_phot, atten, absorp, atten_interp, absorp_interp

def _getCoefficient(E, Z, interpolators):
    """Interpolates NIST cross section data for the given Z"""
    if Z < 1 or Z > 92:
        raise ValueError("Invalid value: Z = %d; Z must be between 1 and 92" % Z)
    elif np.min(E) < 1e-3 or np.max(E) > 2e1:
        raise ValueError("Energy must be between 1 keV and 20 MeV")
    idx1 = np.floor(Z-1).astype('int')
    idx2 = np.ceil(Z-1).astype('int')
    coef1 = interpolators[idx1](E)
    if idx1 == idx2:
        return coef1
    else:
        print("Non-integer Z inputted, interpolating between Z = %d and Z = %d"
              % (np.floor(Z), np.ceil(Z)))
        coef2 = interpolators[idx2](E)
        f = Z % 1
        return f * coef2 + (1 - f) * coef1

def MassAttenCoef(E, Z):
    """Returns the mass attenuation coefficient (cm^2/g) of
    atomic number Z at energy E (in MeV)"""
    return _getCoefficient(E, Z, _atten_interpolators)

def MassEnergyAbsorpCoef(E, Z):
    """Returns the mass energy-absorption coefficient (cm^2/g) of
    atomic number Z at energy E (in MeV)"""
    return _getCoefficient(E, Z, _absorp_interpolators)
