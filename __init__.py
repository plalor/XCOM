import numpy as np
from .utils import loadXsection, buildInterpolator

_CoherentScatterInterpolators = []
_IncoherScatterInterpolators = []
_PhotoelAbsorbInterpolators = []
_NuclearPrPrdInterpolators = []
_ElectronPrPrdInterpolators = []
_TotWCoherentInterpolators = []
_TotWoCoherentInterpolators = []

for Z in range(1, 101):
    filename = "%02d.txt" % Z
    PhotonEnergy_arr, CoherentScatter_arr, IncoherScatter_arr, PhotoelAbsorb_arr, NuclearPrPrd_arr, ElectronPrPrd_arr, TotWCoherent_arr, TotWoCoherent_arr = loadXsection(filename)
    
    _CoherentScatterInterpolators.append(buildInterpolator(PhotonEnergy_arr, CoherentScatter_arr))
    _IncoherScatterInterpolators.append(buildInterpolator(PhotonEnergy_arr, IncoherScatter_arr))
    _PhotoelAbsorbInterpolators.append(buildInterpolator(PhotonEnergy_arr, PhotoelAbsorb_arr))
    _NuclearPrPrdInterpolators.append(buildInterpolator(PhotonEnergy_arr, NuclearPrPrd_arr))
    _ElectronPrPrdInterpolators.append(buildInterpolator(PhotonEnergy_arr, ElectronPrPrd_arr))
    _TotWCoherentInterpolators.append(buildInterpolator(PhotonEnergy_arr, TotWCoherent_arr))
    _TotWoCoherentInterpolators.append(buildInterpolator(PhotonEnergy_arr, TotWoCoherent_arr))

del Z, filename, PhotonEnergy_arr, CoherentScatter_arr, IncoherScatter_arr, PhotoelAbsorb_arr, NuclearPrPrd_arr, ElectronPrPrd_arr, TotWCoherent_arr, TotWoCoherent_arr

def _getCoefficient(E, Z, interpolators):
    """Interpolates NIST cross section data for the given Z"""
    if np.size(Z) > 1:
        return np.array([_getCoefficient(E, Z[i], interpolators) for i in range(np.size(Z))])
    if Z < 1 or Z > 100:
        raise ValueError("Invalid value: Z = %d; Z must be between 1 and 100" % Z)
    if np.min(E) < 1e-3 or np.max(E) > 2e1:
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

def mu_tot(E, Z):
    """Returns the mass attenuation coefficient (cm^2/g) of
    atomic number Z at energy E (in MeV)"""
    return _getCoefficient(E, Z, _TotWCoherentInterpolators)

def mu_PE(E, Z):
    """Returns the photoelectric effect mass attenuation coefficient 
    (cm^2/g) of atomic number Z at energy E (in MeV)"""
    return _getCoefficient(E, Z, _PhotoelAbsorbInterpolators)

def mu_CS(E, Z):
    """Returns the compton scattering mass attenuation coefficient 
    (cm^2/g) of atomic number Z at energy E (in MeV)"""
    return _getCoefficient(E, Z, _IncoherScatterInterpolators)

def mu_PP(E, Z):
    """Returns the pair production mass attenuation coefficient 
    (cm^2/g) of atomic number Z at energy E (in MeV)"""
    return _getCoefficient(E, Z, _NuclearPrPrdInterpolators)
