import torch
import numpy as np
import deepxde as dde
import deepxde.backend as bkd
import pinnicle as pinn
import os

dde.config.set_default_float('float32')

model = 'MCexactHelm'   # for PENN
# model = 'MC'            # for PINN

def capped_MSE(y_true, y_pred): # cap loss with ReLU
    perc = 0.05
    
    se = bkd.square(y_pred-y_true)
    uncert = bkd.square(perc*y_true) # square bc we use mean-SQUARED-error
    capped_se = bkd.relu(se-uncert)
    return bkd.reduce_mean(capped_se)

date = '06-10-26'
if model=='MCexactHelm':
    expNo = 1
elif model=='MC':
    expNo = 2
seeds = [42,84,168,332,664]

for i in np.arange(5):
    seedNo = i+1
    seed = seeds[i]

    path = '<path-to-this-folder>'
    datapath = path + '/data/'
    modelpath = path + '/models/'

    outline = f"{datapath}Byrd-BMap3GL-30ma-vertices.exp"

    bm3 = datapath + 'bedmap3.nc'
    meas = datapath + 'antarctic_ice_vel_phase_map_v01_seconds.nc'

    H_radar = datapath + 'Byrd-ICEBRIDGE-ICECAP-BM3-500m-median-thk.mat'
    apm = datapath + 'apparent_mass_balance_2013-17_mps_masked_grounded.mat'


    outFile = f'Byrd-BMap3GL-30ma-{model}-exp{expNo}-No{seedNo}-{date}' 
    modelFolder = modelpath

    if not os.path.exists(f'{modelFolder}'):
        os.makedirs(f'{modelFolder}')
    if not os.path.exists(f'{modelFolder}/pinn'):
        os.makedirs(f'{modelFolder}/pinn')

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

    MEAS = {}
    MEAS['data_path'] = meas
    MEAS['sample_only_inside'] = True
    MEAS['X_map'] = {'x':'x', 'y':'y'}
    if model in ["MCexactHelm"]:
        MEAS['name_map'] = {'u_MC':'VX', 'v_MC':'VY', 'vel_mag_MC':'VelMag'}
        MEAS['data_size'] = {'u_MC':'MAX', 'v_MC':'MAX', 'vel_mag_MC':'MAX'}
    elif model in ["MC"]:
        MEAS['name_map'] = {'u':'VX', 'v':'VY'} #, 'vel':'VelMag'}
        MEAS['data_size'] = {'u':'MAX', 'v':'MAX'} #, 'vel':'MAX'}
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
    a_loss['function'] = capped_MSE 
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

    hp['mini_batch'] = 200_000

    experiment = pinn.PINN(hp)
    print(experiment.params)

    experiment.compile()

    experiment.train()
    experiment.save_model(name=outFile)
    print(torch.cuda.memory_summary())
    experiment.history.save(path=modelFolder, filename = outFile + f'-700k-history.json')
    experiment.history.plot(path=modelFolder+'/', figname = outFile + f'-700k-history.png')
    print("\n\n\n")