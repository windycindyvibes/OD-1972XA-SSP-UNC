import odlib
import math
import numpy as np

k = 0.0172020989484 #Gaussian gravitational constant
cAU = 173.144643267 #speed of light in au/(mean solar)day
eps = math.radians(23.4374) #Earth's obliquity
order = 4
mu = 1
tolerance = 1E-12
JD_curr = 2459419.7916667

# JPL Values
a_jpl = 1.89340261181919
e_jpl = .5384716698244796
i_jpl = 41.2022527220293
w_jpl = 293.0902755463004
o_jpl = 63.4965666353897 
T_jpl = odlib.get_jd('19:53:35 UT on January 19, 2017')

values_used = []
a_error = []
e_error = []
i_error = []
w_error = []
o_error = []
T_error = []
mean_error = []

filename = 'D:/SSP/OD/2024-1972XA-testinput.txt'

for p in range(0, 7):
    for q in range(p+1, 7):
        for r in range(q+1, 7):
            time = []
            ra = []
            dec = []
            sun = []
            
            with open(filename, 'r') as file:
                lines = file.readlines()
                lines = [lines[p], lines[q], lines[r]]
                for line in lines:
                    line_arr = line.strip().split()
                    time.append(odlib.process_time(line_arr[0], line_arr[1], line_arr[2], line_arr[3]))
                    ra.append(odlib.deg_to_rad(odlib.hours_to_degrees(line_arr[4])))
                    dec.append(odlib.deg_to_rad(odlib.arc_to_degrees(line_arr[5])))
                    sun.append([float(line_arr[6]), float(line_arr[7]), float(line_arr[8])])

            if len(time) > 3:
                indices = str(input("What are the indices of the observations you want? (0 indexed)")).split(',')
                time = [time[indices[0]], time[indices[1]], time[indices[2]]]
                ra = [ra[indices[0]], ra[indices[1]], ra[indices[2]]]
                dec = [dec[indices[0]], dec[indices[1]], dec[indices[2]]]
                sun = [sun[indices[0]], sun[indices[1]], sun[indices[2]]]

            rhohat = []
            for i in range(len(ra)):
                rhohat.append(odlib.get_rhohat(ra[i], dec[i]))

            Ds = odlib.get_Ds(rhohat, sun)
            taus = [k*(time[0]-time[1]), k*(time[2]-time[1]), k*(time[2]-time[0])] # t1, t3, t0
            roots, rhos = odlib.SEL(taus, sun[1], rhohat[1], Ds)

            positive_rhos = sum(1 for x in rhos if x > 0)

            if positive_rhos != 1:
                print('rhos', rhos)
                index = int(input("which rho value do you want? enter a zero-indexed value"))
                if rhos[index] < 0:
                    index = int(input("please select a positive rho value"))
            else:
                for i in range(len(rhos)):
                    if rhos[i] > 0:
                        index = i 

            r2 = roots[index]
            rho = rhos[index]

            f1_i = odlib.get_f_init(r2, taus[0])
            g1_i = odlib.get_g_init(r2, taus[0])
            f3_i = odlib.get_f_init(r2, taus[1])
            g3_i = odlib.get_g_init(r2, taus[1])

            c1_i = g3_i/(f1_i*g3_i-g1_i*f3_i)
            c2_i = -1
            c3_i = -g1_i/(f1_i*g3_i-g1_i*f3_i)

            c_i = [c1_i, c2_i, c3_i]

            d1_i, d3_i = odlib.get_d(f1_i, f3_i, g1_i, g3_i)

            rho_i = odlib.get_rhos(c_i, rhohat, sun)
            r_i = odlib.get_r(rho_i, rhohat, sun)

            r2dot_init = []
            for i in range(len(r_i[0])):
                r2dot_init.append(d1_i*r_i[0][i] + d3_i*r_i[2][i])

            difference = tolerance + 1
            iterations = 0

            rho_init = rho
            rhos_init = rho_i
            r2_init = r_i[1]
            taus_corrected = taus

            while (difference > tolerance and iterations < 10000):
                f1, g1 = odlib.fg(taus_corrected[0], r2_init, r2dot_init, order)
                f3, g3 = odlib.fg(taus_corrected[1], r2_init, r2dot_init, order)

                c1 = g3/(f1*g3-g1*f3)
                c2 = -1
                c3 = -g1/(f1*g3-g1*f3)

                c = [c1, c2, c3]

                d1, d3 = odlib.get_d(f1, f3, g1, g3)

                rho = odlib.get_rhos(c, rhohat, sun)
                r = odlib.get_r(rho, rhohat, sun)

                r2dot = []
                for i in range(len(r[0])):
                    r2dot.append(d1*r[0][i] + d3*r[2][i])
                
                difference = abs(rho[1]-rho_init)
                rho_init = rho[1]
                rhos_init = rho
                iterations += 1
                time_corrected, seconds_corrected = odlib.light_correction(time, rhos_init, cAU)
                taus_corrected = odlib.get_taus(time_corrected, k)
                r2_init = r[1]
                r2dot_init = r2dot

            r2_ecliptic = odlib.equatorial_to_ecliptic(r2_init, eps)
            r2dot_ecliptic = odlib.equatorial_to_ecliptic(r2dot_init, eps)

            r2_converted, r2dot_converted = odlib.AU_to_km(r2_ecliptic, r2dot_ecliptic)

            a = odlib.get_semimajor_axis(r2_converted, r2dot_converted)
            e = odlib.get_eccentricity(r2_converted, r2dot_converted)
            i = odlib.get_inclination(r2_converted, r2dot_converted)
            w = odlib.get_argument(r2_converted, r2dot_converted)
            o = odlib.get_longitude(r2_converted, r2dot_converted)
            n = odlib.get_true_anomaly(r2_converted, r2dot_converted)
            MA_central = odlib.get_mean_anomaly_quad_check(r2_converted, r2dot_converted, n)
            MA_future = odlib.get_mean_anomaly_time_jd_time(JD_curr, time[1], a) + odlib.get_mean_anomaly_quad_check(r2_converted, r2dot_converted, n)
            E = odlib.get_eccentric_anomaly(r2_converted, r2dot_converted)
            perihelion = odlib.get_jd_perihelion_jd_time(JD_curr, a, k, MA_future)

            if not n < math.pi:
                E = 2*math.pi - E

            a_percent_error = odlib.get_percent_error(a_jpl, a)
            e_percent_error = odlib.get_percent_error(e_jpl, e)
            i_percent_error = odlib.get_percent_error(i_jpl, math.degrees(i))
            w_percent_error = odlib.get_percent_error(w_jpl, math.degrees(w))
            o_percent_error = odlib.get_percent_error(o_jpl, math.degrees(o))
            T_percent_error = odlib.get_percent_error(T_jpl, perihelion)

            values_used.append([p,q,r])
            a_error.append(a_percent_error)
            e_error.append(e_percent_error)
            i_error.append(i_percent_error)
            w_error.append(w_percent_error)
            o_error.append(o_percent_error)
            T_error.append(T_percent_error)
            mean_error.append((a_percent_error + e_percent_error + i_percent_error + w_percent_error + o_percent_error + T_percent_error)/6)

min_mean_error = 0
min_mean_error_index = 0

for i in range(len(mean_error)):
    if mean_error[i] < min_mean_error:
        min_mean_error_index = i
        min_mean_error = mean_error[i]

print(min_mean_error)
print(values_used[min_mean_error_index])
