from Cit_par import *
from reduced_condition_calculator import Conditions
from datareader import importExcelData, ThrustingAllDayEveryday
from conversion_helpers import *
from mass_and_balance_input import cg, cg_shifted, dist_to_lemac, mac_length

import numpy as np
import matplotlib.pyplot as plt
import pylab


class Elevator(Conditions):

    def __init__(self, h_p, v_c, t_m, mass):
        Conditions.__init__(self, h_p)
        # Aircraft parameters
        self.s = S
        self.chord = c
        self.c_m_tc = -0.0064
        self.mass_flow_standard = 0.048
        self.weight = mass * self.g0

        # Calculate conditions
        self.calc_pressure()
        self.calc_density()
        self.calc_mach(v_c)
        self.calc_temperature(t_m)
        self.calc_true_airspeed()
        self.calc_equivalent_airspeed()
        self.calc_reduced_airspeed(self.weight)

        # Initializing parameters to calculate
        self.c_n = 0.0
        self.c_m_delta = 0.0
        self.c_m_alpha = 0.0

    def get_reduced_equivalent_airspeed(self):
        return self.reduced_airspeed

    def calc_temperature_difference(self):
        return self.temperature - (self.T0 + (self.lambdas * self.altitude))

    def calc_c_n(self):
        self.c_n = self.weight / (0.5 * self.density * (self.true_airspeed ** 2) * self.s)

        if self.c_n <= 0:
            print "Warning: The aircraft is unstable, c_n = " + str(self.c_n)

        return self.c_n

    def calc_d_c_m(self, x_cg_2, x_cg_1):
        return self.c_n * ((x_cg_2 - x_cg_1) / self.chord)

    def calc_c_m_delta(self, delta_difference, c_m_difference):
        self.c_m_delta = -(c_m_difference / delta_difference)

        if self.c_m_delta >= 0:
            print "Warning: The aircraft is unstable, cm_delta = " + str(self.c_m_delta)
        return self.c_m_delta

    def calc_delta_reduced(self, delta_measured, t_cs, t_c):
        delta_reduced = delta_measured - (1 / self.c_m_delta) * self.c_m_tc * (t_cs - t_c)

        return delta_reduced

    def calc_c_m_alpha(self, derivative):
        self.c_m_alpha = -1 * derivative * self.c_m_delta

        if self.c_m_alpha <= 0:
            print "Warning: The aircraft is unstable, cm_alpha = " + str(self.c_m_alpha)

        return self.c_m_alpha

    def calc_thrust_coefficients(self, mass_flow_l, mass_flow_r):
        delta_temperature = self.calc_temperature_difference()

        standard_input = [self.altitude, self.mach, delta_temperature, self.mass_flow_standard, self.mass_flow_standard]
        thrust_standard = sum(ThrustingAllDayEveryday(standard_input))

        t_cs = thrust_standard / (0.5 * self.density * (self.true_airspeed ** 2) * self.s)

        non_standard_input = [self.altitude, self.mach, delta_temperature, mass_flow_l, mass_flow_r]
        thrust_non_standard = sum(ThrustingAllDayEveryday(non_standard_input))
        t_c = thrust_non_standard / (0.5 * self.density * (self.true_airspeed ** 2) * self.s)

        return t_cs, t_c

    def calc_reduced_delta(self, delta_measured, mass_flow_l, mass_flow_r):
        thrust_cs, thrust_c = self.calc_thrust_coefficients(mass_flow_l, mass_flow_r)

        reduced_delta = delta_measured - (1 / self.c_m_delta) * self.c_m_tc * (thrust_cs - thrust_c)

        return reduced_delta

    def calc_reduced_stick_force(self, force):
        return force * (self.standard_weight / self.weight)


def calc_d_e_d_alpha(trim_curve_data):
    angle_of_attack = []
    elevator_angle = []

    for i in range(len(trim_curve_data)):
        angle_of_attack.append(trim_curve_data[i][4])
        elevator_angle.append(trim_curve_data[i][5])

    z = np.polyfit(angle_of_attack, elevator_angle, 1)
    p = np.poly1d(z)
    derivative = p.deriv()

    # print "the derivative :" + str(der)

    # pylab.plot(alpha, p(alpha), "b")
    # plt.show()

    if derivative < 0:
        print "Warning: The aircraft is unstable, d_e_d_alpha = " + str(derivative)

    return derivative


def calc_weight(start_weight, fuel_used):
    weights = [start_weight]

    for i in range(0, len(fuel_used)):
        weight_left = start_weight - float(fuel_used[i]) * lbs_to_kg
        weights.append(weight_left)

    return weights


# ----------------------------------------------------------------------------------------------------------------------

f_1 = 'Reference_Datasheet.csv'
f_2 = 'Post_Flight_Datasheet_13_03_V2.csv'

trim_curve, old_cg, new_cg, cg_measurements = importExcelData(f_2)[12], importExcelData(f_2)[14], \
                                              importExcelData(f_2)[15], importExcelData(f_2)[16]

starting_weight = (9165. * lbs_to_kg + 2800. * lbs_to_kg + 89. + 82. + 70. + 62. + 74. + 65. + 80. + 82. + 80.)
cg = cg()
cg_shift = cg_shifted()

cg_start = (dist_to_lemac + (cg[0][3]/100)*mac_length)*inch_to_m
cg_end = (dist_to_lemac + (cg_shift[0][0]/100)*mac_length)*inch_to_m

# ----------------------------------------------------------------------------------------------------------------------

cg_weight = calc_weight(starting_weight, [1053., 1082])
elevator_effectiveness = Elevator(cg_measurements[0][2] * ft_to_m, cg_measurements[0][3] * kts_to_ms,
                                  cg_measurements[0][11] + celsius_to_kelvin, cg_weight[0])

elevator_difference = np.radians(cg_measurements[1][5]) - np.radians(cg_measurements[0][5])

c_n = elevator_effectiveness.calc_c_n()
difference_cm = elevator_effectiveness.calc_d_c_m(cg_end, cg_start)  # float(new_cg)*inch_to_m, float(old_cg)*inch_to_m)
cm_delta = elevator_effectiveness.calc_c_m_delta(elevator_difference, difference_cm)

slope = calc_d_e_d_alpha(trim_curve)
cm_alpha = elevator_effectiveness.calc_c_m_alpha(slope)

# ----------------------------------------------------------------------------------------------------------------------

delta = []
speed = []
alpha = []
stick_force = []
weight_values = calc_weight(starting_weight, list(trim_curve[:, -2]))

for j in range(len(trim_curve)):
    m_flow_l = trim_curve[j][8] * lbs_per_hour_to_kg_per_s
    m_flow_r = trim_curve[j][9] * lbs_per_hour_to_kg_per_s
    delta_r = elevator_effectiveness.calc_reduced_delta(trim_curve[j][5], m_flow_l, m_flow_r)

    reducing_elevator = Elevator(trim_curve[j][2] * ft_to_m, trim_curve[j][3] * kts_to_ms,
                                 trim_curve[j][11] + celsius_to_kelvin, weight_values[j])

    airspeed = reducing_elevator.get_reduced_equivalent_airspeed()
    stick_force_reduced = reducing_elevator.calc_reduced_stick_force(trim_curve[j][7])

    alpha.append(trim_curve[j][4])
    speed.append(airspeed)
    stick_force.append(stick_force_reduced)
    delta.append(delta_r)

# ----------------------------------------------------------------------------------------------------------------------

print "c_n equals : " + str(c_n)
print "cm_delta equals : " + str(cm_delta)
print "dcm equals : " + str(difference_cm)
print "cm_alpha equals : " + str(cm_alpha)
# print "The aircraft mass at measurements were : " + str(cg_weight)
# print "The airspeed is : " + str(speed)
# print "The angle of attack is : " + str(alpha)
# print "The elevator angle is : " + str(delta)
# print "The stick force is : " + str(stick_force)

z1 = np.polyfit(speed, delta, 2)
p1 = np.poly1d(z1)

z2 = np.polyfit(alpha, delta, 1)
p2 = np.poly1d(z2)

z3 = np.polyfit(speed, stick_force, 2)
p3 = np.poly1d(z3)

speed.sort()
alpha.sort()

label_font = 20
title_font = 25

plt.figure(1)
plt.grid()
pylab.plot(speed, p1(speed))
plt.gca().invert_yaxis()
plt.xlabel(r"$V_e^*$ [m/s]", fontsize=label_font)
plt.ylabel(r"$\delta_e^*$ [degrees]", fontsize=label_font)
plt.title("Elevator-trim curve", fontsize=title_font)
plt.savefig("trim_curve_velocity")

plt.figure(2)
plt.grid()
pylab.plot(alpha, p2(alpha))
plt.gca().invert_yaxis()
plt.xlabel(r"$\alpha$ [degrees]", fontsize=label_font)
plt.ylabel(r"$\delta_e^*$ [degrees]", fontsize=label_font)
plt.title("Elevator trim curve", fontsize=title_font)
plt.savefig("trim_curve_alpha")

plt.figure(3)
plt.grid()
pylab.plot(speed, p3(speed))
plt.gca().invert_yaxis()
plt.xlabel(r"$V_e^*$ [m/s]", fontsize=label_font)
plt.ylabel(r"$F_e^*$ [N]", fontsize=label_font)
plt.title("Control-force curve", fontsize=title_font)
plt.savefig("control_force_curve")

plt.show()
