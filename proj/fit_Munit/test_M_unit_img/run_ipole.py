import sys
import os
import subprocess

# Parameter Session
mode = 'SPO'

N = 'SgrA'

inc = '30'

# Constant
ipole_dir = f'../../../bin/ipole_{mode}'
par_dir = '../../../par/SgrA.par' 

dsource = [0.008, 9.9, 14, 31, 28]
log_MBH = [6.6, 8.8, 8.9, 9.2, 9.2]
obj = ['SgrA', 'NGC4594', 'NGC3998', 'NGC4261', 'NGC2663']

beta_crit = {'SPO': '5', 'beta': '1'}

dump_dir = '/xdisk/chanc/proj/eht/GRMHD_dt5M/Sa+0.94_w5/torus.out0.05000.h5'
#'/xdisk/rtilanus/proj/eht/GRMHD_kharma-v3/Sa+0.94_w5/torus.out0.05000.h5'
spin = '+0.94'

qshear = '1.9998'
nR = '1.72265'

# Run simulation
n = obj.index(N)
if True:
    M_unit = f"1e{sys.argv[1]}"
    output_dir = f'M_unit/{N}/{mode}/{N}_M{M_unit}_i{inc}.h5'
    print(M_unit, output_dir)
    par = [ipole_dir ,'-par', par_dir, '--M_unit', str(M_unit),
               '--dsource', f"{dsource[n]}e6", '--MBH', str(round(10**log_MBH[n], 4)),
               '--freqcgs', '230.e9', '--thetacam', inc, '--trat_large', "40",
               '--dump', dump_dir, '--fovy_dsource', '50', '--fovx_dsource', '50',
               '--outfile', output_dir,
               '--qshear', qshear, '--nR', nR, 
               '--beta_crit', beta_crit[mode]]

    subprocess.call(par)
