import os
import numpy as np
from typing import Optional
from gliders.plot import *
from gliders.utils import *
from gliders.filter import *
from gliders.updraft import *


def generate_cbu(cbh_clouds, doppler_vel, date, site, class2filter):
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
            #maxlim = np.nanmax(CBU.values)
            #filename = os.path.basename(classification_raw)[:9] + 'hyytiala_updraft_clouds.nc'
            if class2filter == 'ice':
                output_dir_exist = os.path.exists('Output_Clouds_drizzle_' + site)
                if not output_dir_exist:
                    os.makedirs('Output_Clouds_drizzle_' + site)
                filename = date + '_' + site + '_updraft_clouds_drizzle.nc'
                out = 'Output_Clouds_drizzle_' + site + '/' + filename
                CBU.to_netcdf(path=out)

            elif class2filter == 'ice-drizzle':
                output_dir_exist = os.path.exists('Output_Clouds_' + site)
                if not output_dir_exist:
                    os.makedirs('Output_Clouds_' + site)
                filename = date + '_' + site + '_updraft_clouds_only.nc'
                out = 'Output_Clouds_' + site + '/' + filename
                CBU.to_netcdf(path=out)
    return CBU
            
       

def generate_updraft_nc(classification_file: str, categorize_file: str, class2filter:str):
    classification, categorize, site, date = open_files(classification_file, categorize_file)
    cbh, cth = get_height(classification)
    doppler_vel = get_doppler(categorize)
    clouds, aerosols, insects, drizzle, ice, fog = get_classes(classification)
    if class2filter == 'ice':
        clouds_ice_filtered = filter_ice(clouds,ice)
        cbh_clouds = get_filtered_cbh(cbh, clouds_ice_filtered)
        out = generate_cbu(cbh_clouds, doppler_vel, site, date, class2filter)
    elif class2filter == 'ice-drizzle':
        fill_class2filter = drizzle.ffill(dim='time', limit=15).bfill(dim='time', limit=15)
        clouds_filtered = filter_drizzle_ice(clouds,drizzle,ice)
        cbh_clouds = get_filtered_cbh(cbh, clouds_filtered)
        out = generate_cbu(cbh_clouds, doppler_vel, site, date, class2filter)