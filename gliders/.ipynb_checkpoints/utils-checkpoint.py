from cloudnetpy.products import generate_classification
from cloudnetpy.plotting import generate_figure
from unidecode import unidecode
from typing import Optional
import xarray as xr
import pandas as pd
import requests
import fnmatch
import wget
import os





def is_cloudnetpy_dir(site:str, categorize_dir:str='Categorize', classification_dir:str='Classification'):    
    
    """Check if the classification files in a directory are cloudnetpy format.
    If not, generates Cloudnet Level 1b netCDF files from categorize files.
    Needed for legacy data (e.g. Hyytiala 2014-2017) as well as ARM data and other sources. 
    """
    
    for fileclass in os.listdir(classification_dir):
      classification_xrfile = xr.open_dataset(classification_dir + '/' + fileclass)
      classification_cloudnetpy_exist = any('cloudnetpy' in i for i in classification_xrfile.attrs)
      if not classification_cloudnetpy_exist:
        date = fileclass[0:8]
        classification_xrfile.close()
        os.remove(os.path.join(classification_dir,fileclass))
        for filecat in os.listdir(categorize_dir):
          if filecat.startswith(date):
            generate_classification(os.path.join(categorize_dir, filecat), os.path.join(classification_dir, filecat[:8] + '_' + site + '_classification' + '.nc'))

def is_cloudnetpy_file(classification_file: str, categorize_file: str):
  output_name = str(classification_file)
  classification_xrfile = xr.open_dataset(classification_file)
  classification_cloudnetpy_exist = any('cloudnetpy' in i for i in classification_xrfile.attrs)
  if not classification_cloudnetpy_exist:
    classification_xrfile.close()
    os.remove(classification_file)
    generate_classification(categorize_file, output_name)



def open_files(classification_file: str, categorize_file: str):
    is_cloudnetpy_file(classification_file, categorize_file)
    classification = xr.open_dataset(classification_file)
    categorize = xr.open_dataset(categorize_file)
    split = str(categorize.time.values[0])[:10].split('-')
    date = ''.join(split)
    output_name = str(classification_file)
    site = output_name.split('_')[-2]
    #site = ds.attrs['location'].lower()
    #site = unidecode.unidecode(site)
    return classification, categorize, date, site


def get_height(classification_file: str):
    #classification, categorize = open_files(classification_file, categorize_file)
    cbh = classification_file.cloud_base_height_amsl
    cth = classification_file.cloud_top_height_amsl
    return cbh,cth

def get_doppler(categorize):
    doppler_vel = categorize.v
    return doppler_vel
    

def get_classes(classification_file: str):
    
    #classification, categorize = open_files(classification_file, categorize_file)
    classes = classification_file.target_classification
    
    #Subset specific classes
    clouds = classes.where(classes == 1) 
    aerosols = classes.where(classes == 8)
    insects = classes.where((classes == 9) | (classes == 10))
    drizzle = classes.where((classes == 2) | (classes == 3))
    ice = classes.where((classes == 4) | (classes == 5) | (classes == 6) | (classes == 7))
    fog = clouds.where(clouds.height < 400)

    return clouds, aerosols, insects, drizzle, ice, fog


def preprocess(classification_file: str, categorize_file: str):
    is_cloudnetpy_file(classification_file, categorize_file)
    classification = xr.open_dataset(classification_file)
    categorize = xr.open_dataset(categorize_file)
    classes = classification.target_classification
    clouds = classes.where(classes == 1) 
    aerosols = classes.where(classes == 8)
    insects = classes.where((classes == 9) | (classes == 10))
    drizzle = classes.where((classes == 2) | (classes == 3))
    ice = classes.where((classes == 4) | (classes == 5) | (classes == 6) | (classes == 7))
    fog = clouds.where(clouds.height < 400)
    cbh = classification.cloud_base_height_amsl
    return classification, categorize, clouds, aerosols, insects, drizzle, ice, fog, cbh



"""def download_cloudnet(
    site:str, 
    start:str, 
    end:Optional[str] = None, 
    products:list=['categorize','classification',], 
    output_dir:Optional[str]=None):

    
    legacy = ['2011','2012','2013','2014', '2015', '2016', '2017']

    if any(year in start for year in legacy) and (end is None):
      url = 'https://cloudnet.fmi.fi/api/files?site=' + site + '&showLegacy'
      payload = {'date': start, 'product': products}
    elif any(year in start for year in legacy):
      url = 'https://cloudnet.fmi.fi/api/files/?site=' + site + '&dateFrom=' + start + '&dateTo=' + end + '&showLegacy'
      payload = {'product': products}
    elif end is None: 
      url = 'https://cloudnet.fmi.fi/api/files?site=' + site
      payload = {'date': start, 'product': products}
    else:
      url = 'https://cloudnet.fmi.fi/api/files/?site=' + site + '&dateFrom=' + start + '&dateTo=' + end
      payload = {'product': products}
    
    response = requests.get(url, payload)
    data = response.json()
    df = pd.DataFrame(data)
    df = pd.DataFrame(data)
    if df.empty:
      raise Exception("No data available")
    else:
      file = df.downloadUrl

      if output_dir is None:
        classification_exist = os.path.exists('Classification')
        if not classification_exist:
          os.makedirs('Classification')
        
        categorize_exist = os.path.exists('Categorize')
        if not categorize_exist:
          os.makedirs('Categorize')

        for i in file:
          if fnmatch.fnmatch(i, '*classification.nc'):
            filename = os.path.join(os.getcwd(),'Classification' + '/' + os.path.basename(i))
            classification_exist_nc = os.path.exists(filename)
            if not classification_exist_nc:
              wget.download(i, os.path.join(os.getcwd(),'Classification')) # download it to the specific path.
          elif fnmatch.fnmatch(i, '*categorize.nc'):
            filename = os.path.join(os.getcwd(),'Categorize' + '/' + os.path.basename(i))
            categorize_exist_nc = os.path.exists(filename)
            if not categorize_exist_nc:
              wget.download(i, os.path.join(os.getcwd(),'Categorize'))

      else:
        output_dir_exist = os.path.exists(output_dir)
        if not output_dir_exist:
          os.makedirs(output_dir)

        classification_exist_out = os.path.exists(output_dir + '/' + 'Classification')
        if not classification_exist_out:
          os.makedirs(output_dir + '/' + 'Classification')
        
        categorize_exist_out = os.path.exists(output_dir + '/' + 'Categorize')
        if not categorize_exist_out:
          os.makedirs(output_dir + '/' + 'Categorize')

        for i in file:
          if fnmatch.fnmatch(i, '*classification.nc'):
            filename = os.path.join(output_dir,'Classification' + '/' + os.path.basename(i))
            classification_exist_nc = os.path.exists(filename)
            if not classification_exist_nc:
              wget.download(i, output_dir + '/' + 'Classification') # download it to the specific path.
          elif fnmatch.fnmatch(i, '*categorize.nc'):
            filename = os.path.join(output_dir,'Categorize' + '/' + os.path.basename(i))
            categorize_exist_nc = os.path.exists(filename)
            if not categorize_exist_nc:
              wget.download(i, output_dir + '/' + 'Categorize')

    return print(' Done!')  
"""

def download_arm(lidar: None, doppler: None, skycam: None):
    """Download Atmospheric Radiation Measurement (ARM) data
    """


    
    
def download_cloudnet(
    site:str, 
    start:str, 
    end:Optional[str] = None, 
    products:list=['categorize','classification',]):
    
    """Query data from Cloudnet data portal API 
    
    Args:
        site (str): Field site
        start (str): Start date in yyyy-mm-dd (e.g. 2014-02-02)
        end (str): End date in yyyy-mm-dd (for a range of dates if requested)
        products [list]: default products include categorize and classification files
        output_dir (str): download directory 

    Example: download_cloudnet(site='hyytiala', start='2014-08-24', end='2014-08-31', output_dir='Products')

    Reference: https://docs.cloudnet.fmi.fi/api/data-portal.html 
    """ 
    
    legacy = ['2011','2012','2013','2014', '2015', '2016', '2017']

    if any(year in start for year in legacy) and (end is None):
      url = 'https://cloudnet.fmi.fi/api/files?site=' + site + '&showLegacy'
      payload = {'date': start, 'product': products}
    elif any(year in start for year in legacy):
      url = 'https://cloudnet.fmi.fi/api/files/?site=' + site + '&dateFrom=' + start + '&dateTo=' + end + '&showLegacy'
      payload = {'product': products}
    elif end is None: 
      url = 'https://cloudnet.fmi.fi/api/files?site=' + site
      payload = {'date': start, 'product': products}
    else:
      url = 'https://cloudnet.fmi.fi/api/files/?site=' + site + '&dateFrom=' + start + '&dateTo=' + end
      payload = {'product': products}
    
    response = requests.get(url, payload)
    data = response.json()
    df = pd.DataFrame(data)
    df = pd.DataFrame(data)
    if df.empty:
        pass
      #raise Exception("No data available")
    else:
        file = df.downloadUrl
        output_dir_exist = os.path.exists('Products_' + site)
        if not output_dir_exist:
            os.makedirs('Products_' + site)

        classification_exist_out = os.path.exists('Products_' + site + '/' + 'Classification')
        if not classification_exist_out:
            os.makedirs('Products_' + site + '/' + 'Classification')

        categorize_exist_out = os.path.exists('Products_' + site + '/' + 'Categorize')
        if not categorize_exist_out:
            os.makedirs('Products_' + site + '/' + 'Categorize')

        for i in file:
            if fnmatch.fnmatch(i, '*classification.nc'):
                filename = os.path.join('Products_' + site,'Classification' + '/' + os.path.basename(i))
                classification_exist_nc = os.path.exists(filename)
                if not classification_exist_nc:
                    wget.download(i, 'Products_' + site + '/' + 'Classification') # download it to the specific path.
            elif fnmatch.fnmatch(i, '*categorize.nc'):
                filename = os.path.join('Products_' + site,'Categorize' + '/' + os.path.basename(i))
                categorize_exist_nc = os.path.exists(filename)
                if not categorize_exist_nc:
                    wget.download(i, 'Products_' + site + '/' + 'Categorize')

        return print(' ' + site + ' is done!')  


def list_sites(type:str):
    """
    Types are: 
    arm: Atmospheric Radiation Measurement (ARM) site.
    campaign: Temporary measurement sites.
    cloudnet: Official Cloudnet sites.
    hidden: Sites that are not visible in the Cloudnet data portal GUI.
    
    Ref: https://docs.cloudnet.fmi.fi/api/data-portal.html#get-apisites--site
    """
    url = 'https://cloudnet.fmi.fi/api/sites'
    payload = {'type': type}
    response = requests.get(url,payload)
    data = response.json()
    df = pd.DataFrame(data)
    return df

def above_ground(file:str):
    """
    Returns a file with a height above ground level 
    """
    ds = xr.open_dataset(file)
    file_above_ground = ds.assign_coords(height = ds.height - ds.altitude)
    return file_above_ground

def download_cloudnet_all(start:str, end:str):
    """
    Example: download_cloudnet_all(start='2022-08-15', end='2022-08-30')
    """
    df = list_sites('cloudnet')
    sites = list(df.id)
    for site in sites:
        download_cloudnet(site=site, start=start, end=end)