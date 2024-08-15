"""

fit M_unit until the 230 GHz mathces the given observational flux
Change the EPSILON for desired error change
Add the correspoding log_MBH, dsource, mm_Flux of the object
Change the upper limt and lower limit at LEFT and RIGHT
Change the initial guess at INITM_UNIT

"""
import subprocess
import numpy as np
from multiprocessing import Pool
import sys
import os
import h5py
import csv

n = int(sys.argv[1])

EPSILON = 0.005

NGC = ["NGC4594", "NGC4261", "NGC2663", "SgrA"]
log_MBH = [8.8, 8.9, 9.2, 6.6]
dsource = [9.9, 14, 31, 0.008]
mm_Flux = [0.2, 0.13, 0.2, 2.4]

spin = ["+0.94", "+0.5", "0", "-0.5", "-0.94"]
freqcgs = ["230.e9"]#, "230e9", "345e9"]
inclination = ["50", "160"]#, "60", "90"]

nR = ["1.9998", "1.9334", "1.8425", "1.8594", "1.8587"]
qshear = ["1.7265", "1.6539", "1.6332", "1.6548", "1.7477"]

dump_dir = "/xdisk/rtilanus/proj/eht/GRMHD_kharma-v3/Sa"
#dump_dir = '/xdisk/chanc/proj/eht/GRMHD_dt5M/Ma'

LEFT = 1e18
RIGHT = 1e21

INITM_UNIT = 5e19

""" DO NOT CHANGE AFTER THIS LINE """

def run_ipole(a, i, v, M_unit):
    
    avg_unpol = 0
    print(qshear[a], "_", nR[a])
    output_parent_dir = "../img_dump/" + NGC[n] + "_".join([spin[a], freqcgs[v], inclination[i]]) +  "/"
    try:
        os.mkdir(output_parent_dir)
    except OSError as error:
        pass
    try:
        os.mkdir(output_parent_dir + "M_" + str(round(M_unit, 5)))
    except OSError as error:
        pass
    output_dir = output_parent_dir + "M_" + str(round(M_unit, 5)) +"/"
    for fno in range(10):
        par = ['../../../bin/ipole' ,'-par', '../../../par/SgrA.par', '--M_unit', str(M_unit),
               '--dsource', str(dsource[n])+"e6", '--MBH', str(round(10**log_MBH[n], 4)),
               '--freqcgs', freqcgs[v], '--thetacam', str(inclination[i]), '--trat_large', "40",
               '--dump', dump_dir + spin[a] + "_w5/torus.out0.05" + str(fno) + "00.h5",
               '--outfile', output_dir + str(fno) + "000.h5",
               '--qshear', qshear[a], '--nR', nR[a], '-unpol']
        print(par)
        subprocess.run(par)
        hfp = h5py.File(output_dir + str(fno) + "000.h5")
        scale = hfp['header']['scale'][()]
        unpol = np.copy(hfp['unpol']).transpose((1, 0)).sum()*scale
        with open(output_dir + "log.csv", 'a') as log:
                write = csv.writer(log)
                write.writerow([str(fno), str(unpol)])

        avg_unpol += unpol
    avg_unpol /= 10

    return avg_unpol

def bisection(a, i, v, init_M_unit, left_init, right_init):
    left = left_init
    right = right_init
    Munit = init_M_unit

    calc_flux = run_ipole(a, i, v, init_M_unit)

    while abs(calc_flux - mm_Flux[n]) > EPSILON:
        if calc_flux < mm_Flux[n]:
            left = Munit
        else:
            right = Munit
        Munit = (left + right)/2
        calc_flux = run_ipole(a, i, v, Munit)
    return Munit

def iter(param):
    a, i, v = param

    newMunit = bisection(a, i, v, INITM_UNIT, LEFT, RIGHT)
    print(newMunit)
    return (spin[a], inclination[i], freqcgs[v], newMunit, NGC[n])

if __name__ == "__main__":
    #a = spin.index("+0.94")
    #param = [(a, i, v) for a in range(len(spin))
    #                   for i in range(len(inclination))
    #                   for v in range(len(freqcgs))]

    param = [(spin.index("+0.5"), inclination.index("160"), freqcgs.index("230.e9"))]

    with Pool() as pool:
        row = pool.map(iter, param)
    import csv
    with open("M_unit.csv", 'a') as f:
        write = csv.writer(f)
        write.writerows(row)

    

