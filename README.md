# XCOM

XCOM is a simple tool for loading in and interpolating NIST photon cross section data into Python (https://physics.nist.gov/PhysRefData/XrayMassCoef/tab3.html)

## Usage

XCOM offers two functions, `MassAttenCoef` and `MassEnergyAbsorpCoef` which return the mass attenuation coefficient (https://physics.nist.gov/PhysRefData/XrayMassCoef/chap2.html) and mass energy-absorption coefficient (https://physics.nist.gov/PhysRefData/XrayMassCoef/chap3.html), respectively, for a given energy `E` (in MeV) and atomic number `Z`.

## To run:

```python
import sys
sys.path.append("/path/to/XCOM/")
from XCOM import MassAttenCoef, MassEnergyAbsorpCoef

E = 2e-1  # 200 keV
Z = 92    # Uranium
coef = MassAttenCoef(E, Z)
```
