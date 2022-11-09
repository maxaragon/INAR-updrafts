# INAR-updrafts :cloud:

## Python implementation for retrieving cloud base vertical velocities using Cloudnet data[^1]


Create virtual environment:

    python -m venv INAR

Activate virtual environment (Windows):

    INAR/Scripts/activate
    
Activate virtual environment (Mac):

    source INAR/bin/activate
    
Install required libraries:

    pip install -r requirements.txt
    
Add the environment to Jupyter:

    ipython kernel install --user --name=INAR

## BAECC directory includes:


* nc_files_drizzle: Doppler velocities at the cloud base including drizzle (ice clouds filtered)
* nc_files_clouds: Doppler velocities at the cloud base only liquid clouds (ice clouds and drizzle filtered)

* pdf_clouds: PDF liquid clouds only
* pdf_drizle: PDF including drizzle

* vertical_vel_drizzle: Quick lookup figures of vertical velocities including drizzle
* vertical_vel_clouds: Quick lookup figures of vetical velocities of liquid clouds only


[^1]: https://cloudnet.fmi.fi/
