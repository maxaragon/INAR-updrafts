
import os
import glob
import xarray as xr
import pandas as pd




def filter_drizzle_ice(clouds,drizzle,ice):
    

    #########################
    # Filter drizzle
    #########################
    
    # Fill drizzle horizontal gaps (time) every 15 mins (limit 15 = 7.5min since 1 = 30s [therefore, filling 7.5 mins before and 7.5 mins after])
    fill_drizzle = drizzle.ffill(dim='time', limit=15).bfill(dim='time', limit=15)
    # Expand drizzle vertically (height) 300m above and 300m below (limit 10 = 300, since 1 = 30m)
    expand_drizzle = fill_drizzle.ffill(dim='height', limit=10).bfill(dim='time', limit=10)
    # Only liquid water without overlapping drizzle (Remove liquid clouds with drizzle)
    clouds_out_drizzle = clouds.where(~clouds.notnull() == expand_drizzle.notnull())
    # Fill horizontally liquid clouds out of drizzle
    fill_clouds_out_drizzle = clouds_out_drizzle.ffill(dim='time', limit=10).bfill(dim='time', limit=10)
    # Only liquid clouds overlapping drizzle
    clouds_in_drizzle = clouds.where(clouds.notnull() == expand_drizzle.notnull())  
    # Expand vertically liquid clouds in drizzle vertically
    expand_clouds_in_drizzle=clouds_in_drizzle.ffill(dim='height',limit=7).bfill(dim='height',limit=7).ffill(dim='time',
                                                                                                             limit=10).bfill(dim='time',limit=10)
    # Connect cloud-drizzle expansions
    clouds_drizzle_connect = fill_clouds_out_drizzle.where(fill_clouds_out_drizzle.notnull() == expand_clouds_in_drizzle.notnull())  
    # Remove those time slices with connections
    clouds_no_drizzle_time = clouds_drizzle_connect.dropna(dim='time', how='all', thresh=None)
    # Get liquid clouds without without ice
    clouds_only_no_drizzle = clouds_out_drizzle.where(~clouds_out_drizzle.time.isin(clouds_no_drizzle_time.time))
    
    #########################
    # Filter ice clouds
    #########################
    
    fill_ice = ice.ffill(dim='time', limit=15).bfill(dim='time', limit=15)
    # Expand ice to 510 m above and below
    expand_ice = fill_ice.ffill(dim='height', limit=17).bfill(dim='height', limit=17)
    #Only liquid water without overlapping ice
    cloudsO = clouds_only_no_drizzle.where(~clouds_only_no_drizzle.notnull() == expand_ice.notnull())
    # Only liquid clouds opverlapping ice
    cloudsf = clouds_only_no_drizzle.where(clouds_only_no_drizzle.notnull() == expand_ice.notnull())
    # Expand liquid clouds overlapping ice 
    cloudsH = cloudsf.ffill(dim='height', limit=7).bfill(dim='height', limit=7).ffill(dim='time', limit=10).bfill(dim='time', limit=10)
    # Expand liquid clouds without overlapping ice
    cloudsOX = cloudsO.ffill(dim='time', limit=10).bfill(dim='time', limit=10)
    # Connect cloud expansions
    cloudsC = cloudsOX.where(cloudsOX.notnull() == cloudsH.notnull())
    # Remove liquid clouds below ice
    cloudsC2 = cloudsC.dropna(dim='time', how='all', thresh=None)
    # Get liquid clouds without without ice
    cloudsC3 = cloudsO.where(~cloudsO.time.isin(cloudsC2.time))
    # Fill gaps in liquid clouds
    cloudsC4 = cloudsC3.ffill(dim='time', limit=2).bfill(dim='time', limit=2)
    clouds_filtered = cloudsC4.dropna(dim='time', how='all').dropna(dim='height', how='all')
    return clouds_filtered, cloudsC3 



def filter_ice(clouds,ice):
    fill_ice = ice.ffill(dim='time', limit=15).bfill(dim='time', limit=15)
    # Expand ice to 510 m above and below
    expand_ice = fill_ice.ffill(dim='height', limit=17).bfill(dim='height', limit=17)
    #Only liquid water without overlapping ice
    cloudsO = clouds.where(~clouds.notnull() == expand_ice.notnull())
    # Only liquid clouds opverlapping ice
    cloudsf = clouds.where(clouds.notnull() == expand_ice.notnull())
    # Expand liquid clouds overlapping ice 
    cloudsH = cloudsf.ffill(dim='height', limit=7).bfill(dim='height', limit=7).ffill(dim='time', limit=10).bfill(dim='time', limit=10)
    # Expand liquid clouds without overlapping ice
    cloudsOX = cloudsO.ffill(dim='time', limit=10).bfill(dim='time', limit=10)
    # Connect cloud expansions
    cloudsC = cloudsOX.where(cloudsOX.notnull() == cloudsH.notnull())
    # Remove liquid clouds below ice
    cloudsC2 = cloudsC.dropna(dim='time', how='all', thresh=None)
    # Get liquid clouds without without ice
    cloudsC3 = cloudsO.where(~cloudsO.time.isin(cloudsC2.time))
    # Fill gaps in liquid clouds
    cloudsC4 = cloudsC3.ffill(dim='time', limit=2).bfill(dim='time', limit=2)
    clouds_ice_filtered = cloudsC4.dropna(dim='time', how='all').dropna(dim='height', how='all')
    return clouds_ice_filtered, cloudsC3
 


def get_filtered_cbh(cbh,clouds_filtered):
    cbh_clouds = cbh.where(cbh.notnull() == clouds_filtered.notnull())
    return cbh_clouds

def generate_library(path):
    '''
    
    Rank files based on draft abundance 'drafts' and mean velocities 'mean'
    
    '''
    # check if the path exists
    if not os.path.exists(path):
        raise ValueError(f'{path} does not exist')
    # Initialize an empty list to store the data
    data = []

    # Iterate over the list of file paths
    for i in glob.glob(path + '/*.nc'):
        # Open the file and get the length of u3.v
        ds = xr.open_dataset(i)
        v_len = len(ds.v)
        m1 = float(ds.v.mean().values); v_mean = round(m1,4)

        # Store the file path and the length of u3.v in a tuple
        data.append((i, v_len, v_mean))

    # Create a pandas data frame from the data
    df = pd.DataFrame(data, columns=['date', 'drafts', 'mean_v'])
    
    min_val = df["drafts"].min()
    max_val = df["drafts"].max()

    min_val_m = df["mean_v"].min()
    max_val_m = df["mean_v"].max()
    
    df["drafts_normal"] = (df["drafts"] - min_val) / (max_val - min_val)
    df["mean_v_normal"] = (df["mean_v"] - min_val_m) / (max_val_m - min_val_m)
    
    df["score"] = df["drafts_normal"] + df["mean_v_normal"]
    
    df = df.sort_values(['score'], ascending=[False])
    
    
    def extract_date(file_name):
        return file_name.split('/')[3].split('_')[0]

    df['date'] = df['date'].apply(extract_date)
    
    return df