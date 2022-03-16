import numpy as np
from scipy.interpolate import interp1d
import pkgutil

def loadXsection(filename):
    """Loads NIST cross section data"""    
    data = pkgutil.get_data(__name__, "data/%s" % filename).decode("utf-8")
    data_arr = data.split("\n")[3:-1]    
    n = len(data_arr)
    
    PhotonEnergy_arr = np.zeros(n)
    CoherentScatter_arr = np.zeros(n)
    IncoherScatter_arr = np.zeros(n)
    PhotoelAbsorb_arr = np.zeros(n)
    NuclearPrPrd_arr = np.zeros(n)
    ElectronPrPrd_arr = np.zeros(n)
    TotWCoherent_arr = np.zeros(n)
    TotWoCoherent_arr = np.zeros(n)

    for i in range(n):
        PhotonEnergy, CoherentScatter, IncoherScatter, PhotoelAbsorb, NuclearPrPrd, ElectronPrPrd, TotWCoherent, TotWoCoherent = data_arr[i].split()
        PhotonEnergy_arr[i] = PhotonEnergy
        CoherentScatter_arr[i] = CoherentScatter
        IncoherScatter_arr[i] = IncoherScatter
        PhotoelAbsorb_arr[i] = PhotoelAbsorb
        NuclearPrPrd_arr[i] = NuclearPrPrd
        ElectronPrPrd_arr[i] = ElectronPrPrd
        TotWCoherent_arr[i] = TotWCoherent
        TotWoCoherent_arr[i] = TotWoCoherent
    
    ### Changing resonances so they don't have identical x values
    for i in range(n-1):
        if PhotonEnergy_arr[i] == PhotonEnergy_arr[i+1]:
            energyStr = np.format_float_scientific(PhotonEnergy_arr[i], precision=5)
            idx = energyStr.find("e")
            energyPrefix = energyStr[:idx]
            energySuffix = energyStr[idx:]
            energyPrefixNew = str(float(energyPrefix) - 1e-5)
            PhotonEnergy_arr[i] = float(energyPrefixNew + energySuffix)
    
    return PhotonEnergy_arr, CoherentScatter_arr, IncoherScatter_arr, PhotoelAbsorb_arr, NuclearPrPrd_arr, ElectronPrPrd_arr, TotWCoherent_arr, TotWoCoherent_arr

def buildInterpolator(x, y):
    """Returns a function that takes energy as input and
    returns the corresponding attenuationg using log-log
    interpolation from arguments 'energy' and 'coef'"""
    with np.errstate(divide='ignore'):
        interpRaw = interp1d(np.log(x), np.log(y))
    interp = lambda x: np.exp(interpRaw(np.log(x)))
    return interp
