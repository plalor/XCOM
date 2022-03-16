# XCOM

XCOM is a simple tool for loading in and interpolating NIST photon cross section data into Python (https://physics.nist.gov/PhysRefData/Xcom/html/xcom1.html)

## Usage

The mass attenuation coefficient is expressed as a sum of the mass attenuation coefficients from the photoelectric effect (PE), Compton scattering (CS), and pair production (PP). XCOM offers four functions: `mu_PE`, `mu_CS`, `mu_PP`, and `mu_tot`, which return the corresponding mass attenuation coefficient (cm^2/g) at a given energy `E` (in MeV) and atomic number `Z`.

See more at https://physics.nist.gov/PhysRefData/XrayMassCoef/chap2.html

## To run:

```python
import sys
sys.path.append("/path/to/XCOM/")
from XCOM import mu_tot

E = 2e-1  # 200 keV
Z = 92    # Uranium
coef = mu_tot(E, Z)
```
