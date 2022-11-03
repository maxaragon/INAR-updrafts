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
