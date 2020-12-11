A simple tool for loading in and interpolating XCOM photon cross section data

Usage:

>> import sys
>> sys.path.append("/path/to/XCOM/")
>> from XCOM import getMassAtten

Then, if you want the mass attenuation coefficient (with units cm^2/g) for atomic number 'Z' at energy 'E' (in MeV):

>> atten = getMassAtten(E, Z)
