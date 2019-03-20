# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
#                               Imports
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
from math import *
from matplotlib import pyplot as plt
from datareader import *
from Cit_par import S, g, A
from conversion_helpers import lbs_to_kg, lbs_per_hour_to_kg_per_s, celsius_to_kelvin, kts_to_ms, ft_to_m
from elevator_effectiveness import Elevator, calc_weight

CL_CD_series1 = importExcelData('Post_Flight_Datasheet_13_03_V2.csv')[9]


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
#                               Weight calculations
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
weight_zero = (9165. + 2800. + 89. + 82. + 70. + 62. + 74. + 65. + 80. + 82. + 80.)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
#                               CL calculations
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def CL(CL_CD_series1, start_weight, s):
    # Input: datareader file [no adjustments required], mass [kg], wing surface area [m^2]
    calibrated_speed = CL_CD_series1[:, 3] * kts_to_ms
    t_measured = CL_CD_series1[:, -1]
    t_measured += celsius_to_kelvin
    altitude = CL_CD_series1[:, 2] * ft_to_m
    m_flow_l = CL_CD_series1[:, 5] * lbs_per_hour_to_kg_per_s
    m_flow_r = CL_CD_series1[:, 6] * lbs_per_hour_to_kg_per_s
    fuel_used = CL_CD_series1[:, 7] * lbs_to_kg
    weight = calc_weight(start_weight, fuel_used)

    Cl = []
    Cd = []
    x = []
    delta_t = []

    for k in range(len(altitude)):
        # Find the true airspeed [m/s]
        elevator = Elevator(altitude[k], calibrated_speed[k], t_measured[k], weight[k])
        temp_difference = elevator.calc_temperature_difference()
        delta_t.append(temp_difference)

        true_speed = elevator.true_airspeed
        density = elevator.density

        # Calculate CL for each time interval (and convert mass [kg] to weight [N])
        non_standard_input = [elevator.altitude, elevator.mach, delta_t[k], m_flow_l[k], m_flow_r[k]]
        thrust = sum(ThrustingAllDayEveryday(non_standard_input))

        Cl.append(weight[k] * g / (1. / 2 * (true_speed ** 2) * s * density))

        Cd.append(2 * thrust / (density * S * true_speed ** 2))
        x.append(Cl[k] ** 2)

    # Output: array with CL values at each time interval
    # Obtain slope of CD CL^2 diagram to find the Oswald factor
    slope = np.polyfit(x, Cd, 1, full=False)[0]
    oswald_factor = 1. / (pi * A * slope)

    # Get CD_zero from the intersection with the y-axis
    CD_zero = np.polyfit(x, Cd, 1, full=False)[1]

    # Output: array with CD values at each time interval; CD_zero; oswald factor
    return Cl, Cd, CD_zero, oswald_factor


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
#                               Plots
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def Plots(Cl, Cd, alpha):
    # Plot CL against angle of attack
    plt.figure()
    plt.plot(alpha, Cl)
    plt.title('CL-alpha')
    plt.xlabel('Angle of attack [degrees]')
    plt.ylabel('CL [-]')
    plt.show()

    # Plot CD against angle of attack
    plt.figure()
    plt.plot(alpha, Cd)
    plt.title('CD-alpha')
    plt.xlabel('Angle of attack [degrees]')
    plt.ylabel('CD [-]')
    plt.show()

    # Plot CD against CL
    plt.figure()
    plt.plot(Cl, Cd)
    plt.title('CD-CL')
    plt.xlabel('CL [-]')
    plt.ylabel('CD [-]')
    plt.show()
    return


alpha = list(CL_CD_series1[:, 4])
Cl, Cd, Cd_zero, oswald_factor = CL(CL_CD_series1, weight_zero, S)
Plots(Cl, Cd, alpha)
