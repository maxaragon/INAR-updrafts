import os
import numpy as np
import xarray as xr
from tqdm import tqdm
from typing import Optional
from gliders.plot import *
from gliders.utils import *
from gliders.filter import *
from gliders.updraft import *


def generate_cbu(cbh_clouds, doppler_vel, date, site, class2filter=None):
    
    """
    Generates cloud base updraft product.
    This function retrieves doppler velocities at the base of warm clouds. 
    Results are written in a netCDF file.
    """

    if np.count_nonzero(~np.isnan(cbh_clouds)) == 0:
        pass
    else:
        v_cbh_clouds = doppler_vel.where(doppler_vel.time.isin(cbh_clouds.time), drop = True)
        v_cbh_clouds_max_min_clean = v_cbh_clouds.dropna(dim='height', how='all')
        vel = v_cbh_clouds_max_min_clean; 
        CBU = vel.where((vel.height < cbh_clouds + 100) & (vel.height > cbh_clouds - 100))
        if np.count_nonzero(~np.isnan(CBU)) < 10:
            pass
        else:
            if class2filter == 'ice':
                output_dir_exist = os.path.exists('Products_' + site + '/' + 'Updraft' + '/' + 'output_2_' + site)
                if not output_dir_exist:
                    os.makedirs('Products_' + site + '/' + 'Updraft' + '/' + 'output_2_' + site)
                filename = date + '_' + site + '_updraft_2.nc'
                out = 'Products_' + site + '/' + 'Updraft' + '/' + 'output_2_' + site + '/' + filename
                updraft_exist_nc = os.path.exists(out)
                if not updraft_exist_nc:
                    CBU.close()
                    CBU.to_netcdf(path=out)
                else:
                    pass

            elif class2filter == 'ice-drizzle':
                output_dir_exist = os.path.exists('Products_' + site + '/' + 'Updraft' + '/' + 'output_3_' + site)
                if not output_dir_exist:
                    os.makedirs('Products_' + site + '/' + 'Updraft' + '/' + 'output_3_' + site)
                filename = date + '_' + site + '_updraft_3.nc'
                out = 'Products_' + site + '/' + 'Updraft' + '/' + 'output_3_' + site + '/' + filename
                updraft_exist_nc = os.path.exists(out)
                if not updraft_exist_nc:
                    CBU.close()
                    CBU.to_netcdf(path=out)
                else:
                    pass
                
            elif class2filter is None:
                output_dir_exist = os.path.exists('Products_' + site + '/' + 'Updraft' + '/' + 'output_1_' + site)
                if not output_dir_exist:
                    os.makedirs('Products_' + site + '/' + 'Updraft' + '/' + 'output_1_' + site)
                filename = date + '_' + site + '_updraft_1.nc'
                out = 'Products_' + site + '/' + 'Updraft' + '/' + 'output_1_' + site + '/' + filename
                updraft_exist_nc = os.path.exists(out)
                if not updraft_exist_nc:
                    CBU.close()
                    CBU.to_netcdf(path=out)
                else:
                    pass
            
       
    

def generate_updraft_nc(classification_file: str, categorize_file: str, class2filter=None):
    try:
        classification, categorize, date, site = open_files(classification_file, categorize_file)
    except:
        pass
    else:
        cbh, cth = get_height(classification)
        doppler_vel = get_doppler(categorize)
        classes, clouds, aerosols, insects, drizzle, ice, fog = get_classes(classification)
        if class2filter == 'ice':
            clouds_ice_filtered,cloudsC3 = filter_ice(clouds,ice)
            cbh_clouds = get_filtered_cbh(cbh, clouds_ice_filtered)
            out = generate_cbu(cbh_clouds, doppler_vel, date, site, class2filter)
        elif class2filter == 'ice-drizzle':
            clouds_filtered,cloudsC3 = filter_drizzle_ice(clouds,drizzle,ice)
            cbh_clouds = get_filtered_cbh(cbh, clouds_filtered)
            out = generate_cbu(cbh_clouds, doppler_vel, date, site, class2filter)
        elif class2filter is None:
            cbh_clouds = get_filtered_cbh(cbh,clouds)
            out = generate_cbu(cbh_clouds, doppler_vel, date, site, class2filter=None)
    #print(f'Done {classification_file}')
        
        
def nonupdraft(classification_path, categorize_path, updraft_path):
    
    """
    
    Returns non-updraft dates
    
    """
    
    output_name = os.listdir(classification_path)[0]
    site = output_name.split('_')[-2]
    
    class_dates = []
    
    for classification, categorize in tqdm(zip(sorted(filter(lambda x: os.path.isfile(os.path.join(classification_path,x)),os.listdir(classification_path))), sorted(filter(lambda x: os.path.isfile(os.path.join(categorize_path, x)),os.listdir(categorize_path))))):
        assert len(os.listdir(classification_path)) == len(os.listdir(categorize_path))
        generate_updraft_nc(os.path.join(classification_path, classification), os.path.join(categorize_path, categorize), 'ice-drizzle')
        class_dates.append(classification.split('_')[0])
    
    updraft_dates = []
    for file in os.listdir(updraft_path + '/' + 'output_3_' + site):
        updraft_dates.append(file.split('_')[0])
        
    
    nonupdrafts = []
    for element in class_dates:
        if element not in updraft_dates:
            nonupdrafts.append(element) 
    
    return nonupdrafts, site


def keep_updrafts(classification_path, categorize_path, updraft_path):
    nonupdrafts, site = nonupdraft(classification_path, categorize_path, updraft_path)
    purge(classification_path, nonupdrafts)
    purge(categorize_path, nonupdrafts)
    for classification, categorize in tqdm(zip(sorted(filter(lambda x: os.path.isfile(os.path.join(classification_path,x)),os.listdir(classification_path))), sorted(filter(lambda x: os.path.isfile(os.path.join(categorize_path, x)),os.listdir(categorize_path))))):
        assert len(os.listdir(classification_path)) == len(os.listdir(categorize_path))
        generate_updraft_nc(os.path.join(classification_path, classification), os.path.join(categorize_path, categorize))
        generate_updraft_nc(os.path.join(classification_path, classification), os.path.join(categorize_path, categorize), 'ice')
        
    out3 = []

    for file in os.listdir(updraft_path + '/' + 'output_3_' + site):
        out3.append(file.split('_')[0])

    out2 = []

    for file in os.listdir(updraft_path + '/' + 'output_2_' + site):
        out2.append(file.split('_')[0])

    out1 = []

    for file in os.listdir(updraft_path + '/' + 'output_1_' + site):
        out1.append(file.split('_')[0])



    nonout = []
    for element in out3:
        if element not in out1:
            nonout.append(element)

    for element in out2:
        if element not in out1:
            nonout.append(element)

    final = [*set(nonout)]
    
    purge(updraft_path + '/' + 'output_1_' + site, final)
    purge(updraft_path + '/' + 'output_2_' + site, final)
    purge(updraft_path + '/' + 'output_3_' + site, final)
    purge(classification_path, final)
    purge(categorize_path, final)
    
