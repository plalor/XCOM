import numpy as np
from scipy.interpolate import interp1d
import pkgutil

def loadXsection(filename):
    """Loads NIST cross section data"""
    #path = "/path/to/XCOM/data/"
    #E_phot, atten = np.loadtxt(path + filename, skiprows=2).T
    
    data = pkgutil.get_data(__name__, "data/%s" % filename).decode("utf-8")
    E_phot = []
    atten = []
    for row in data.split("\n")[3:]:
        enrg, att = row.split()
        E_phot.append(float(enrg))
        atten.append(float(att))
    E_phot = np.array(E_phot)
    atten = np.array(atten)
    
    ### Changing resonances so they don't have identical x values
    for i in range(len(E_phot)-1):
        if E_phot[i] == E_phot[i+1]:
            energyStr = np.format_float_scientific(E_phot[i], precision=4)
            idx = energyStr.find("e")
            energyPrefix = energyStr[:idx]
            energySuffix = energyStr[idx:]
            energyPrefixNew = str(float(energyPrefix) - 0.001)
            energyNew = energyPrefixNew + energySuffix
            E_phot[i] = energyNew
    
    return E_phot, atten

def buildInterpolator(energy, atten):
    """Returns a function that takes energy as input and
    returns the corresponding attenuationg using log-log
    interpolation from arguments 'energy' and 'atten'"""
    interpRaw = interp1d(np.log(energy), np.log(atten))
    interp = lambda enrg: np.exp(interpRaw(np.log(enrg)))
    return interp
