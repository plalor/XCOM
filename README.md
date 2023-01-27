# XCOM

XCOM is a simple tool for loading in and interpolating NIST photon cross section data into Python (https://physics.nist.gov/PhysRefData/Xcom/html/xcom1.html)

## Usage

The attenuation of photons through a material is described by the Beer-Lambert law

I / I_0 = exp(-mu(E, Z) * lambda)

where mu(E, Z) is the mass attenuation coefficient. In the MeV energy range, photon interactions are dominated by the the photoelectric effect (PE), Compton scattering (CS), and pair production (PP). XCOM offers five functions: `mu_PE(E, Z)`, `mu_CS(E, Z)`, `mu_PP(E, Z)`, `mu_tot(E, Z)`, and `mu_en(E, Z)` which return the corresponding mass attenuation coefficient (cm^2/g) at a given energy `E` (in MeV) and atomic number `Z`.

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
