"""
Python 3.7.7
Austin Brandenberger

Setup:
Given a known resistor and an unknown capacitor, setup a RC, CR and an RCR circuit.
Then input an AC signal with frequencies varying from 10^2 to 10^6 hz
Collect the voltage data between the resistor and the capacitor-This is the frequency response data

Solve for the transfer function (Voltage at the collection location as a function of frequency)
Fit the function to the data with capacitance as a free parameter using scipy.curve_fit()
Average the fit values to find the capacitance
The capacitor is supposed to be 100nF, but this program is supposed to treat as a general situation. with upper
and lower limits for the predicted capacitance. It will not consistently work for any capacitor above a few microfarrad.

completed spring 2021
"""

import setuptools
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#importing a .txt file of my frequency response data
#xdata is frequency in hz, ydata is Va in volts
RC_f, RC_v = np.loadtxt("RCdata.txt", unpack=True)
CR_f, CR_v = np.loadtxt("CRdata.txt", unpack=True)
RCR_f, RCR_v = np.loadtxt("RCRdata.txt", unpack=True)

#defining known Variables of my transfer function
v_rc = 3.535 #volts
v_cr =3.543
v_rcr = 3.477
r = 1475 #ohms
r2 = 1197
"""these are my transfer functions for the circuits"""
def RCfit(RC_f ,c): #c is the free parameter
    w = RC_f*2*np.pi #converting f to omega
    Va = v_rc*(1/(1+(w*c*r)**2))**.5
    return Va
def CRfit(CR_f, c):
    w = CR_f*2*np.pi #converting f to omega
    Va = v_cr*(1/(1+1/(w*c*r)**2))**.5
    return Va
def RCRfit(RCR_f, c):
    w = RCR_f*2*np.pi #converting f to omega
    Va = v_rcr*r2*((r**2+1/(w*c)**2)/((r*r2)**2+((r+r2)**2)/(w*c)**2))**.5
    return Va

"""Curve Fitting for capacitance"""
#I had to set bounds for the curve fitting proecess otherwise the values would run negative or be way too large
popt_rc , pcov_rc = curve_fit(RCfit, RC_f, RC_v , bounds = [0, 1])
popt_cr , pcov_cr = curve_fit(CRfit, CR_f, CR_v, bounds = [0, 1])
popt_rcr , pcov_rcr = curve_fit(RCRfit, RCR_f, RCR_v, bounds = [0, 1*10**-6]) #I had to change my guess to get it to properly fit. 
#popt is an array that stores our parameter c in that order so that p[0] = c

"""Values for capacitance, the free parameter"""
print('C1:', popt_rc*10**9, 'nF')
print('C2:', popt_cr*10**9, 'nF')
print('C3:', popt_rcr*10**9, 'nF')
print('C average:', (popt_rc[0]+popt_cr[0]+popt_rcr[0])/3*10**9, 'nF')

c1 = 'C1: ' + str(popt_rc[0]*10**9) + ' nF'
c2 = 'C2: ' + str(popt_cr[0]*10**9) + ' nF'
c3 = 'C3: ' + str(popt_rcr[0]*10**9) + ' nF'
"""Plots of the data and the fit"""
plt.rcParams.update({'font.size': 22})
#RC plots
#plt.subplot(131)
plt.title('RC Fit')
plt.plot(RC_f, RC_v, 'k.', label = 'rc data')
plt.plot(RC_f,RCfit(RC_f, popt_rc[0]), color = 'fuchsia', label = 'rc fit')
plt.ylabel('Voltage [V]')
plt.xlabel('Frequency [Hz]')
plt.xscale('log')
plt.xlim(10, 10**6)
plt.ylim(0, 5)
plt.text(25,4.85, c1)
plt.legend(loc='best')
plt.grid()
plt.show()

#CR plots
#plt.subplot(132)
plt.title('CR Fit')
plt.plot(CR_f, CR_v, 'k.', label = 'cr data')
plt.plot(CR_f, CRfit(CR_f, popt_cr[0]), color = 'crimson', label = 'cr fit')
plt.ylabel('Voltage [V]')
plt.xlabel('Frequency [Hz]')
plt.xscale('log')
plt.xlim(10, 10**6)
plt.ylim(0, 5)
plt.text(25,4.85, c2)
plt.legend(loc='best')
plt.grid()
plt.show()

#RCR plots
#plt.subplot(133)
plt.title('RCR Fit')
plt.plot(RCR_f, RCR_v, 'k.', label = 'rcr data')
plt.plot(RCR_f, RCRfit(RCR_f, popt_rcr[0]), color = 'crimson', label = 'rcr fit')
plt.ylabel('Voltage [V]')
plt.xlabel('Frequency [Hz]')
plt.xscale('log')
plt.xlim(10, 10**6)
plt.ylim(0, 5)
plt.text(25,4.85, c3)
plt.legend(loc='best')
plt.grid()

plt.show()

