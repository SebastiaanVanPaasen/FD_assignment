# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:12:34 2019

@author: daanv
"""

from datareader import getFDValues,importExcelData,convertToSec,convertToTimeStr
import matplotlib.pyplot as plt

keylist,desclist,unitlist,newDict = getFDValues('reference.mat')

date_of_flight, flight_number, TO_time, LND_time, passengerMass, passengerNames\
, passengerPos, blockfuel, ACC_CLCD, CL_CD_series1, CL_CD_series2, ACC_Trim,\
 El_Trim_Curve, name_shifted, pos_shifted, newpos_shifted, Cg_shift, eigenmotions\
 = importExcelData('Reference_Datasheet.csv')


# eigenmotions - phugoid, short period, dutch roll,\
# dutch roll Yd, aperiodic Roll, Spiral
lengths = [200.,60.,40.,60.,60.,60.]
modes = ["Phugoid", "short period", "dutch roll","dutch roll Yd", "aperiodic Roll", "Spiral" ]
label_font = 20
title_font = 25
def time_stamps(n):
    #n is which eigenmode is to be plotted
    time_start = convertToSec(eigenmotions[n])
    time_end = time_start+lengths[n]
    
    indices = []
    for i in range(len(time_list)):
        if time_start<time_list[i]<time_end:
            indices.append(i)
    return indices
    
time_list = newDict.get("time") 
velocity_list = newDict.get("Dadc1_tas")
altitude_list = newDict.get("Dadc1_alt")
alpha_list = newDict.get("vane_AOA")
roll_list = newDict.get("Ahrs1_Roll")
yaw_list = newDict.get("Ahrs1_Pitch")

######phugoid (n=0): plotting speed, altitude and angle of attack against time
n = 0
indices = time_stamps(n)    
 
plt.figure()    
ax1 = plt.subplot(311)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("True airspeed [m/s]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],velocity_list[indices[0]:indices[-1]])
ax2 = plt.subplot(312, sharex = ax1)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("Pressure altitude [m]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],altitude_list[indices[0]:indices[-1]])
ax3 = plt.subplot(313,sharex = ax1)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("angle of attack [deg]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],alpha_list[indices[0]:indices[-1]])

plt.suptitle(modes[n], fontsize = title_font)  
plt.show()

######short period (n=1): plotting speed, altitude and angle of attack against time 

n=1
indices = time_stamps(n)    
       
plt.figure()       
plt.subplot(311)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("True airspeed [m/s]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],velocity_list[indices[0]:indices[-1]])
plt.subplot(312)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("Pressure altitude [m]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],altitude_list[indices[0]:indices[-1]])
plt.subplot(313)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("angle of attack [deg]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],alpha_list[indices[0]:indices[-1]])
plt.suptitle(modes[n], fontsize = title_font)  
plt.show()


#####dutch roll (n=2): plot yaw angle, roll angle, altitude and true airspeed
n=2
indices = time_stamps(n)    
       
plt.figure()       
plt.subplot(221)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("True airspeed [m/s]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],velocity_list[indices[0]:indices[-1]])
plt.subplot(222)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("Pressure altitude [m]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],altitude_list[indices[0]:indices[-1]])
plt.subplot(223)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("yaw angle [deg]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],yaw_list[indices[0]:indices[-1]])
plt.subplot(224)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("roll angle [deg]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],roll_list[indices[0]:indices[-1]])
plt.suptitle(modes[n], fontsize = title_font)  
plt.show()

#####dutch roll YD (n=3): plot yaw angle, roll angle, altitude and true airspeed
n=3
indices = time_stamps(n)    
       
plt.figure()       
plt.subplot(221)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("True airspeed [m/s]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],velocity_list[indices[0]:indices[-1]])
plt.subplot(222)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("Pressure altitude [m]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],altitude_list[indices[0]:indices[-1]])
plt.subplot(223)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("yaw angle [deg]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],yaw_list[indices[0]:indices[-1]])
plt.subplot(224)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("roll angle [deg]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],roll_list[indices[0]:indices[-1]])
plt.suptitle(modes[n], fontsize = title_font)  
plt.show()

#####aperiodic roll (n=4): plot yaw angle, roll angle, altitude and true airspeed
n=4
indices = time_stamps(n)    
       
plt.figure()       
plt.subplot(221)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("True airspeed [m/s]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],velocity_list[indices[0]:indices[-1]])
plt.subplot(222)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("Pressure altitude [m]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],altitude_list[indices[0]:indices[-1]])
plt.subplot(223)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("yaw angle [deg]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],yaw_list[indices[0]:indices[-1]])
plt.subplot(224)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("roll angle [deg]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],roll_list[indices[0]:indices[-1]])
plt.suptitle(modes[n], fontsize = title_font)  
plt.show()

#####spiral (n=5): plot yaw angle, roll angle, altitude and true airspeed
n=5
indices = time_stamps(n)    
       
plt.figure()       
plt.subplot(221)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("True airspeed [m/s]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],velocity_list[indices[0]:indices[-1]])
plt.subplot(222)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("Pressure altitude [m]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],altitude_list[indices[0]:indices[-1]])
plt.subplot(223)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("yaw angle [deg]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],yaw_list[indices[0]:indices[-1]])
plt.subplot(224)
plt.xlabel("time [sec]", fontsize = label_font)
plt.ylabel("roll angle [deg]", fontsize = label_font)
plt.plot(time_list[indices[0]:indices[-1]],roll_list[indices[0]:indices[-1]])
plt.suptitle(modes[n], fontsize = title_font)  
plt.show()