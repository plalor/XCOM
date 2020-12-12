A simple tool for loading in and interpolating NIST photon cross section data (https://physics.nist.gov/PhysRefData/XrayMassCoef/tab3.html)

Usage:

>> import sys
>> sys.path.append("/path/to/XCOM/")
>> from XCOM import MassAttenCoef, MassEnergyAbsorpCoef

Then, if you want the mass attenuation coefficient (with units cm^2/g) for atomic number 'Z' at energy 'E' (in MeV):

>> E = 2e-1  # 200 keV
>> Z = 92    # Uranium
>> coef = MassAttenCoef(E, Z)
