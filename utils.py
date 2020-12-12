import numpy as np
from scipy.interpolate import interp1d
import pkgutil

def loadXsection(filename):
    """Loads NIST cross section data"""
    data = pkgutil.get_data(__name__, "data/%s" % filename).decode("utf-8").split("\n")
    E_phot = []
    atten = []
    absorp = []
    for i in range(10, len(data)):
        row = data[i].split()
        if len(row) == 3:
            E_phot.append(float(row[0]))
            atten.append(float(row[1]))
            absorp.append(float(row[2]))
        elif len(row) == 4:
            E_phot.append(float(row[1]))
            atten.append(float(row[2]))
            absorp.append(float(row[3]))
    E_phot = np.array(E_phot)
    atten = np.array(atten)
    absorp = np.array(absorp)
    ### Changing resonances so they don't have identical x values
    for i in range(len(E_phot)-1):
        if E_phot[i] == E_phot[i+1]:
            energyStr = np.format_float_scientific(E_phot[i], precision=5)
            idx = energyStr.find("e")
            energyPrefix = energyStr[:idx]
            energySuffix = energyStr[idx:]
            energyPrefixNew = str(float(energyPrefix) - 1e-5)
            E_phot[i] = float(energyPrefixNew + energySuffix)
    return E_phot, atten, absorp

def buildInterpolator(energy, coef):
    """Returns a function that takes energy as input and
    returns the corresponding attenuationg using log-log
    interpolation from arguments 'energy' and 'coef'"""
    interpRaw = interp1d(np.log(energy), np.log(coef))
    interp = lambda enrg: np.exp(interpRaw(np.log(enrg)))
    return interp
