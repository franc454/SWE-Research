# -*- coding: utf-8 -*-
"""
Liquid Water Content Equation Solver

Equations used are from 'Measuring Snow Liquid Water Content with Low-Cost 
GPS Receivers' by Koch et al. 2014.

Author: Keenen Francois-King
"""

import numpy as np
from scipy.optimize import fsolve

#constants
rho_w = 1000 #density of water [kg/m^3]
rho_ds = 370 #density of dry snow [kg/m^3]
rho_i = 917 #density of ice [kg/m^3]
freq = 1.57542e9 #Frequency of L1-band waves recieved at GPS [GHz]
eps_a_prime = 1.0 #permittivity of air at 0 °C and a frequency of 1 GHz
eps_i_prime = 3.18 #permittivity of ice at 0 °C and a frequency of 1 GHz
eps_w_prime = 88 #permittivity of water at 0 °C and a frequency of 1 GHz
eps_w_dub_prime = 9.8 #imaginary part of the complex permittivity of water at 0 °C and a frequency of 1 GHz
eps_0 = 8.8541878176e-12 #electric field constant [F/m]
mu_0 = 1.25663706e-6 #magnetic constant [(m*kg/(s^2*A^2))]
Zv = np.sqrt(mu_0/eps_0) #free-space wave impedence



class LWE():
    
    def __init__(self, x):
        self.time = x[0] #time [UTC: hhmmss]. Not used in equations but is returned in the
                                #output to keep time and LWC values together.
        self.Im1 = float(x[1]) #SNR above snow [dB]
        self.Im23 = float(x[2]) #SNR below snow [dB]
        self.d = float(x[3]) #snow depth [m]
        self.theta_elev = float(x[4])
        #converting theta_elev to theta_0
        self.theta_0 = float(np.radians(90-self.theta_elev))

    #Function for calculating LWE using the empirical formula for eps_s_prime via Sihvola and Tiuri   
    def solve_equations(self):
        
        def f_sihvola(theta_w_sihvola):
            #real part of complex permittivity of snow
            eps_s_prime = 1 + (1.7e-3)*rho_ds+(7.0e-7)*rho_ds**2+(8.7e-2)*theta_w_sihvola+(7.0e-3)*theta_w_sihvola**2
            #imaginary part of complex permittivity of snow
            eps_s_dub_prime = (freq/(10**9))*((1.0e-3)*theta_w_sihvola+((8.0e-5)*theta_w_sihvola**2))*eps_w_dub_prime
            #depth wave travels through snow
            ds = (self.d)/(np.cos(np.arcsin(np.sin(self.theta_0/np.sqrt(eps_s_prime)))))
            #angle of refraction of wave entering snow
            theta_refr = (np.arcsin(np.sin(self.theta_0/np.sqrt(eps_s_prime))))
            #wave impedence for snow
            Zs = np.sqrt(mu_0/(eps_0*(eps_s_prime+eps_s_dub_prime)))
            #parallel reflection coefficient
            r_parr = (Zv*np.cos(self.theta_0)-Zs*np.cos(theta_refr))/(Zv*np.cos(self.theta_0)+Zs*np.cos(theta_refr))
            #perpendicular reflection coefficient
            r_perp = (Zs*np.cos(self.theta_0) - Zv*np.cos(theta_refr))/(Zs*np.cos(self.theta_0) + Zv*np.cos(theta_refr))
            ##mean reflected intensity
            Ir = ((r_perp**2 + r_parr**2)/2)*self.Im1
            #attenuation of a medium like snow
            attenuation1 = np.sqrt(mu_0/(eps_s_prime*eps_0))*eps_s_dub_prime*eps_0*2*np.pi*freq
            #additional representation of homogenous medium as assumed for snow.  Applies
            #Beer-Lambert's Law
            attenuation2 = -np.log(self.Im23/(self.Im1-Ir))/ds
            #setting attenuation equations equal to solve for theta_w_sihvola
            set_equal = attenuation1 - attenuation2
    
            return set_equal
        
        #fsolve finds the roots of an equation and returns them.  The roots in sihvola, denoth and roth are
        #theta_w_sihvola, theta_w_denoth and theta_w_roth respectively, which are the liquid water content values.
        theta_w_sihvola = fsolve(f_sihvola, 0.01)
        theta_w_sihvola, f_sihvola(theta_w_sihvola)


    #Function for calculating LWE using the empirical formula for eps_s_prime via Denoth
        def f_denoth(theta_w_denoth):
    
            rho_ws = rho_ds +(0.01*theta_w_denoth*rho_w)
            eps_s_prime = 1+(1.92e-3)*rho_ws+(4.4e-7)*(rho_ws)**2 + (1.87e-1)*theta_w_denoth+(4.5e-3)*theta_w_denoth**2
            eps_s_dub_prime = (freq/(10**9))*((1.0e-3)*theta_w_sihvola+((8.0e-5)*theta_w_sihvola**2))*eps_w_dub_prime
            ds = (self.d)/(np.cos(np.arcsin(np.sin(self.theta_0/np.sqrt(eps_s_prime)))))
            theta_refr = (np.arcsin(np.sin(self.theta_0/np.sqrt(eps_s_prime))))
            Zs = np.sqrt(mu_0/eps_0*(eps_s_prime+eps_s_dub_prime))
            r_parr = (Zv*np.cos(self.theta_0)-Zs*np.cos(theta_refr))/(Zv*np.cos(self.theta_0)+Zs*np.cos(theta_refr))
            r_perp = (Zs*np.cos(self.theta_0) - Zv*np.cos(theta_refr))/(Zs*np.cos(self.theta_0) + Zv*np.cos(theta_refr))
            Ir = ((r_perp**2 + r_parr**2)/2)*self.Im1

            attenuation1 = np.sqrt(mu_0/(eps_s_prime*eps_0))*eps_s_dub_prime*eps_0*2*np.pi*freq
            attenuation2 = -np.log(self.Im23/(self.Im1-Ir))/ds
            set_equal = attenuation1 - attenuation2
    
            return set_equal
    
        theta_w_denoth = fsolve(f_denoth, 0.01)
        theta_w_denoth, f_denoth(theta_w_denoth)   

 
    #Function for calculating LWE using the empirical formula for eps_s_prime via Roth et al.
        def f_roth(theta_w_roth):
    
            eps_s_prime = (0.01*theta_w_roth*(eps_w_prime**0.5)+(rho_ds/rho_i)*(eps_i_prime**0.5)+(1-(rho_ds/rho_i)-0.01*theta_w_roth)*(eps_a_prime**0.5))**2
            eps_s_dub_prime = (freq/(10**9))*((1.0e-3)*theta_w_sihvola+((8.0e-5)*theta_w_sihvola**2))*eps_w_dub_prime
            ds = (self.d)/(np.cos(np.arcsin(np.sin(self.theta_0/np.sqrt(eps_s_prime)))))
            theta_refr = (np.arcsin(np.sin(self.theta_0/np.sqrt(eps_s_prime))))
            Zs = np.sqrt(mu_0/eps_0*(eps_s_prime+eps_s_dub_prime))
            r_parr = (Zv*np.cos(self.theta_0)-Zs*np.cos(theta_refr))/(Zv*np.cos(self.theta_0)+Zs*np.cos(theta_refr))
            r_perp = (Zs*np.cos(self.theta_0) - Zv*np.cos(theta_refr))/(Zs*np.cos(self.theta_0) + Zv*np.cos(theta_refr))
            Ir = ((r_perp**2 + r_parr**2)/2)*self.Im1

            attenuation1 = np.sqrt(mu_0/(eps_s_prime*eps_0))*eps_s_dub_prime*eps_0*2*np.pi*freq
            attenuation2 = -np.log(self.Im23/(self.Im1-Ir))/ds
            set_equal = attenuation1 - attenuation2
    
            return set_equal

        theta_w_roth = fsolve(f_roth, 0.01)
        theta_w_roth, f_roth(theta_w_roth)

        return [self.time, theta_w_sihvola[0], theta_w_denoth[0], theta_w_roth[0]]
#       