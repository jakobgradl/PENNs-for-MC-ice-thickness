import torch
import numpy as np
import deepxde as dde
import deepxde.backend as bkd
import pinnicle as pinn
import os

dde.config.set_default_float('float32')

## Set 'model' and 'seedNo' variables 

model = 'MCexactHelm'   # for PENN
# model = 'MC'            # for PINN
seedNo = 1 # choose from 1 to 5
expNo = 1
date = '06-10-26'


## some paramters
seeds = [42,84,168,332,664]
seed = seeds[seedNo-1]


## paths to data files

path = '<path-to-folder>'
datapath = path + '/data/'
modelpath = path + '/models/'

outline = datapath + "Byrd-BMap3GL-30ma-vertices.exp"

meas = datapath + 'antarctic_ice_vel_phase_map_v01.nc' # MEaSUREs velocity

H_radar = datapath + 'Byrd-ICEBRIDGE-ICECAP-BM3-500m-median-thk.mat' # run make-bm3-thk-files.ipynb
apm = datapath + 'apparent_mass_balance_2013-17_mps.mat' # run make-amb.ipynb

# for validation experiments
H_radar_synth = datapath + 'exp1-ice-thickness-BedMap-grid-holdout-60KMspacing-synthetic-train.mat'
meas_synth = datapath + 'exp1-surface-velocity-Measures-grid-synthetic.mat'
apm_synth = datapath + 'exp1-apparent-mass-balance-BedMap-grid-synthetic.mat'


outFile = f'Byrd-BMap3GL-30ma-{model}-exp{expNo}-No{seedNo}-{date}' 
modelFolder = modelpath

if not os.path.exists(f'{modelFolder}'):
    os.makedirs(f'{modelFolder}')
if not os.path.exists(f'{modelFolder}/pinn'):
    os.makedirs(f'{modelFolder}/pinn')

## PINNICLE parameter dictionary

hp = {}
hp['epochs'] = 700_000 

hp['learning_rate'] = 1.e-3
hp['decay_rate'] = 0
hp['decay_steps'] = 10_000

hp["random_seed"] = seed

if model=='MC':
    loss_list = ['MSE'] + 2*['MAE'] + 2*['MSE'] # fMC,u,v,a,H
    hp['loss_functions'] = loss_list
    MC = {}
    MC['pde_weights'] = [1e16]
    MC['data_weights'] = [1e8, 1e8, 1e21, 1e-3] # u,v,a,H
    hp["equations"] = {"MC":MC}
else:
    hp['loss_functions'] = []
    hp['loss_weights'] = []
    MC_exact_Helmholtz = {} # [D, R, H]
    MC_exact_Helmholtz['data_weights'] = [1.0]*2 + [1.0e-3]
    hp["equations"] = {"MC_exact_Helmholtz":MC_exact_Helmholtz}

hp['save_path'] = modelFolder
hp['is_save'] = False
hp['is_plot'] = True

hp["activation"] = "SiLU"
hp["initializer"] = "Glorot uniform"
hp["num_neurons"] = 50
hp["num_layers"] = 8

hp['shapefile'] = outline
hp['num_collocation_points'] = 2_000
hp["period"] = 5

yts = pinn.physics.Constants().yts

MEAS = {}
MEAS['data_path'] = meas
MEAS['sample_only_inside'] = True
MEAS['X_map'] = {'x':'x', 'y':'y'}
if model in ["MCexactHelm"]:
    MEAS['name_map'] = {'u_MC':'VX', 'v_MC':'VY'}
    MEAS['data_size'] = {'u_MC':'MAX', 'v_MC':'MAX'}
    MEAS['scaling'] = {"u_MC":1.0/yts, "v_MC":1.0/yts} # convert to m/s
elif model in ["MC"]:
    MEAS['name_map'] = {'u':'VX', 'v':'VY'}
    MEAS['data_size'] = {'u':'MAX', 'v':'MAX'}
    MEAS['scaling'] = {"u":1.0/yts, "v":1.0/yts}
MEAS['source'] = 'nc'

APM = {}
APM['data_path'] = apm
APM['sample_only_inside'] = True
APM['X_map'] = {'x':'x', 'y':'y'}
if model in ["MC"]:
    APM['name_map'] = {'a':'a-2013-17'}
    APM['data_size'] = {'a':'MAX'}
elif model in ["MCexactHelm"]:
    APM['name_map'] = {'smb_MC':'a-2013-17'}
    APM['data_size'] = {'smb_MC':'MAX'}
APM['source'] = 'mat'

H = {}
H['data_path'] = H_radar
H['sample_only_inside'] = True
H['X_map'] = {'x':'x', 'y':'y'}
if model in ["MC"]:
    H['name_map'] = {'H':'median-thickness'}
    H['data_size'] = {'H':'MAX'} 
elif model in ["MCexactHelm"]:
    H['name_map'] = {'H_MC':'median-thickness'}
    H['data_size'] = {'H_MC':'MAX'}
H['source'] = 'mat'

## synthetic data for validation experiments
MEAS_SYNTH = {}
MEAS_SYNTH['data_path'] = meas_synth
MEAS_SYNTH['sample_only_inside'] = True
MEAS_SYNTH['X_map'] = {'x':'x', 'y':'y'}
MEAS_SYNTH['name_map'] = {'u_MC':'vx', 'v_MC':'vy'}
MEAS_SYNTH['data_size'] = {'u_MC':'MAX', 'v_MC':'MAX'}
MEAS_SYNTH['source'] = 'mat'

APM_SYNTH = {}
APM_SYNTH['data_path'] = apm_synth
APM_SYNTH['sample_only_inside'] = True
APM_SYNTH['X_map'] = {'x':'x', 'y':'y'}
APM_SYNTH['name_map'] = {'smb_MC':'app_mb'}
APM_SYNTH['data_size'] = {'smb_MC':'MAX'}
APM_SYNTH['source'] = 'mat'

H_SYNTH = {}
H_SYNTH['data_path'] = H_radar_synth
H_SYNTH['sample_only_inside'] = True
H_SYNTH['X_map'] = {'x':'x', 'y':'y'}
H_SYNTH['name_map'] = {'H_MC':'ice_thickness'}
H_SYNTH['data_size'] = {'H_MC':'MAX'} 
H_SYNTH['source'] = 'mat'


H_loss = {}
H_loss['name'] = "H"
H_loss['function'] = "MSE" 
H_loss['weight'] = 1.0e-3

u_loss = {}
u_loss['name'] = "u"
u_loss['function'] = "MAE"
u_loss['weight'] = 1.0e8 

v_loss = {}
v_loss['name'] = "v"
v_loss['function'] = "MAE" 
v_loss['weight'] = 1.0e8

a_loss = {}
a_loss['name'] = "a"
a_loss['function'] = "MSE"
a_loss['weight'] = 1.0e21 

if model in ["MCexactHelm"]:
    hp["additional_loss"] = {
        "u_MC":u_loss, 
        "v_MC":v_loss,
        "H_MC":H_loss,
        "smb_MC":a_loss
        }
elif model in ["MC","MC_SSA","MC_SSAweak"]:
    pass

hp['data'] = {
    'MEAS':MEAS, 
    'H':H, 
    'APM':APM
    }

## validation experiments, uncomment to run
# hp['data'] = {
    # 'MEAS_SYNTH':MEAS_SYNTH, 
    # 'H_SYNTH':H_SYNTH, 
    # 'APM_SYNTH':APM_SYNTH
    # }

hp['mini_batch'] = 200_000

## run model

experiment = pinn.PINN(hp)
print(experiment.params)

experiment.compile()

experiment.train()
experiment.save_model(name=outFile)
print(torch.cuda.memory_summary())
experiment.history.save(path=modelFolder, filename = outFile + f'-700k-history.json')
experiment.history.plot(path=modelFolder+'/', figname = outFile + f'-700k-history.png')
print("\n\n\n")