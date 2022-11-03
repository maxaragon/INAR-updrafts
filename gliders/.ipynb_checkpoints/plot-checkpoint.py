import matplotlib.dates as mdates
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime 
from gliders.utils import *
from gliders.updraft import *
import xarray as xr
import numpy as np
import seaborn as sns

def plot_raw(classification_file,categorize_file):
    classification, categorize, date, site = open_files(classification_file, categorize_file)
    
    classes = classification.target_classification
    
    cbh, cth = get_height(classification)
    
    #Subset specific classes
    clouds = classes.where(classes == 1) 
    drizzle = classes.where((classes == 2) | (classes == 3))
    ice = classes.where((classes == 4) | (classes == 5) | (classes == 6) | (classes == 7))
    clouds_drizzle_ice = classes.where((classes == 1) | (classes == 2) | (classes == 3) | (classes == 4) | (classes == 5) | (classes == 6) | (classes == 7));
    clouds_drizzle_ice.values[clouds_drizzle_ice.values == 3] = 2
    clouds_drizzle_ice.values[clouds_drizzle_ice.values == 4] = 3
    clouds_drizzle_ice.values[clouds_drizzle_ice.values == 5] = 3
    clouds_drizzle_ice.values[clouds_drizzle_ice.values == 6] = 3
    clouds_drizzle_ice.values[clouds_drizzle_ice.values == 7] = 3
    
    def cbh_clouds(cbh,clouds):
        cbh_clouds = cbh.where(cbh.notnull() == clouds.notnull())
        return cbh_clouds
    
    fig, (ax1) = plt.subplots(1, figsize=(12, 3), sharey=True, sharex=True)
    myFmt = mdates.DateFormatter('%H')
    ax1.xaxis.set_major_formatter(myFmt)

    cmap = mpl.colors.ListedColormap(['#00D1FF', '#B276FF', 'grey'])
    norm = mpl.colors.BoundaryNorm([1, 2, 3, 4], cmap.N)
    x = np.arange(0.5,4)
    pcm = clouds_drizzle_ice.plot(x='time', ax=ax1, cmap=cmap, norm=norm, add_colorbar=False)
    cbar = fig.colorbar(pcm, orientation="vertical", ax=ax1, ticks=x)
    cbar.set_ticklabels(['Clouds', 'Droplets', 'Drizzle', 'Ice'])
    
    
    def startx(classes):
        date = str(classes.time.data[0])[0:10]
        time =str(classes.time.data[0])[11:16]
        y = date + ' ' + time
        startx = datetime.strptime(y, "%Y-%m-%d %H:%M")
        return startx
    
    def endx(classes):
        date = str(classes.time.data[-1])[0:10]
        time =str(classes.time.data[-1])[11:16]
        y = date + ' ' + time
        endx = datetime.strptime(y, "%Y-%m-%d %H:%M")
        return endx
    
    for ax in [ax1]:
        ax.set_ylim([0, np.nanmax(cbh_clouds(cbh,clouds)) + 1500])
        ax.set_xlim([startx(classes), endx(classes)])
        ax.set_title(str(classification.time[0].values)[:10], loc='left')
        ax.set_title(site.capitalize())
        ax.set_ylabel('Height above mean sea level (m)')
        ax.set_xlabel('Time (UTC)')
    for label in ax.get_xticklabels():
        label.set_rotation(0);
        
def plot_filters(classification_file,categorize_file):
    classification, categorize, date, site = open_files(classification_file, categorize_file)
    
    classes = classification.target_classification
    
    cbh, cth = get_height(classification)
    
    #Subset specific classes
    clouds = classes.where(classes == 1) 
    drizzle = classes.where((classes == 2) | (classes == 3))
    ice = classes.where((classes == 4) | (classes == 5) | (classes == 6) | (classes == 7))
    
    clouds_drizzle_ice = classes.where((classes == 1) | (classes == 2) | (classes == 3) | (classes == 4) | (classes == 5) | (classes == 6) | (classes == 7));
    clouds_drizzle_ice.values[clouds_drizzle_ice.values == 3] = 2
    clouds_drizzle_ice.values[clouds_drizzle_ice.values == 4] = 3
    clouds_drizzle_ice.values[clouds_drizzle_ice.values == 5] = 3
    clouds_drizzle_ice.values[clouds_drizzle_ice.values == 6] = 3
    clouds_drizzle_ice.values[clouds_drizzle_ice.values == 7] = 3
    
    clouds_ice_filtered, cloudsC3 = filter_ice(clouds,ice)
    #clouds_filtered, cloudsC3  = filter_drizzle_ice(clouds,drizzle,ice)
    
    def cbh_clouds(cbh,clouds):
        cbh_clouds = cbh.where(cbh.notnull() == clouds.notnull())
        return cbh_clouds
    
    
    # Prepare the figure
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(21, 4), sharey=True, sharex=True, gridspec_kw={'width_ratios': [3.5, 3, 3]})

    myFmt = mdates.DateFormatter('%H')

    for ax in [ax1,ax2,ax3]:
        ax.xaxis.set_major_formatter(myFmt)

    cmap = mpl.colors.ListedColormap(['#00D1FF', '#B276FF', 'grey'])
    norm = mpl.colors.BoundaryNorm([1, 2, 3, 4], cmap.N)
    x = np.arange(0.5,4)
    pcm = clouds_drizzle_ice.plot(x='time', ax=ax1, cmap=cmap, norm=norm, add_colorbar=False)
    cbar = fig.colorbar(pcm, orientation="vertical", ax=ax1, ticks=x)
    cbar.set_ticklabels(['Clouds', 'Droplets', 'Drizzle', 'Ice'])

    cmap = mpl.colors.ListedColormap(['#00D1FF'])
    cloudsC3.plot(x='time', ax=ax2, add_colorbar=False, cmap=cmap)
    ax2.set_ylabel('')
    ax2.set_title('Ice filtered')

    clouds_filtered, cloudsC3  = filter_drizzle_ice(clouds,drizzle,ice)
    cmap = mpl.colors.ListedColormap(['#00D1FF'])
    cloudsC3.plot(x='time', ax=ax3, add_colorbar=False, cmap=cmap)
    ax3.set_ylabel('')
    ax3.set_title('Ice and drizzle filtered')

    
    def startx(classes):
        date = str(classes.time.data[0])[0:10]
        time =str(classes.time.data[0])[11:16]
        y = date + ' ' + time
        startx = datetime.strptime(y, "%Y-%m-%d %H:%M")
        return startx
    
    def endx(classes):
        date = str(classes.time.data[-1])[0:10]
        time =str(classes.time.data[-1])[11:16]
        y = date + ' ' + time
        endx = datetime.strptime(y, "%Y-%m-%d %H:%M")
        return endx
    
    for ax in [ax1]:
        ax.set_ylim([0, np.nanmax(cbh_clouds(cbh,clouds)) + 1500])
        ax.set_ylabel('Height above mean sea level (m)')
        ax.set_xlim([startx(classes), endx(classes)])
        ax.set_title(str(classification.time[0].values)[:10], loc='left')
        ax.set_title(site.capitalize(), loc='right')
        ax.set_title('Raw data')
        
    for ax in [ax1,ax2,ax3]:
        ax.set_xlabel('Time (UTC)')
        for label in ax.get_xticklabels():
            label.set_rotation(0)
    
def plot_filters_v(classification_file,categorize_file):
    classification, categorize, date, site = open_files(classification_file, categorize_file)
    
    classes = classification.target_classification
    
    cbh, cth = get_height(classification)
    
    #Subset specific classes
    clouds = classes.where(classes == 1) 
    drizzle = classes.where((classes == 2) | (classes == 3))
    ice = classes.where((classes == 4) | (classes == 5) | (classes == 6) | (classes == 7))
    
    clouds_ice_filtered, cloudsC3 = filter_ice(clouds,ice)
    #clouds_filtered, cloudsC3  = filter_drizzle_ice(clouds,drizzle,ice)
    
    def cbh_clouds(cbh,clouds):
        cbh_clouds = cbh.where(cbh.notnull() == clouds.notnull())
        return cbh_clouds
    
    
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(10, 5), sharey=True, sharex=True, gridspec_kw={'wspace': 2})
    myFmt = mdates.DateFormatter('%H')
    
    for ax in [ax1, ax2, ax3]:
        ax.xaxis.set_major_formatter(myFmt)
    
    cmap = mpl.colors.ListedColormap(['#00D1FF'])
    clouds.plot(x='time', ax=ax1, add_colorbar=False, cmap=cmap)
    
    cmap = mpl.colors.ListedColormap(['grey'])
    ice.plot(x='time', ax=ax1, add_colorbar=False, cmap=cmap)

    cmap = mpl.colors.ListedColormap(['#B276FF'])
    drizzle.plot(x='time', ax=ax1, add_colorbar=False, cmap=cmap)
    ax1.yaxis.set_label_coords(-0.1, -0.7)
    ax1.set_xlabel('')
    
    
    cmap = mpl.colors.ListedColormap(['b'])
    cloudsC3.plot(x='time', ax=ax2, add_colorbar=False, cmap=cmap)
    ax2.set_ylabel('')
    ax2.set_xlabel('')
    
    clouds_filtered, cloudsC3  = filter_drizzle_ice(clouds,drizzle,ice)
    cmap = mpl.colors.ListedColormap(['b'])
    cloudsC3.plot(x='time', ax=ax3, add_colorbar=False, cmap=cmap)
    ax3.set_ylabel('')
    
    
    
    def startx(classes):
        date = str(classes.time.data[0])[0:10]
        time =str(classes.time.data[0])[11:16]
        y = date + ' ' + time
        startx = datetime.strptime(y, "%Y-%m-%d %H:%M")
        return startx
    
    def endx(classes):
        date = str(classes.time.data[-1])[0:10]
        time =str(classes.time.data[-1])[11:16]
        y = date + ' ' + time
        endx = datetime.strptime(y, "%Y-%m-%d %H:%M")
        return endx
    
    for ax in [ax1]:
        ax.set_ylim([0, np.nanmax(cbh_clouds(cbh,clouds)) + 1500])
        ax.set_xlim([startx(classes), endx(classes)])
        ax.set_title(str(classification.time[0].values)[:10], loc='left')
        ax.set_title(site.capitalize())
        
    for ax in ax3.get_xticklabels():
            ax.set_rotation(0)
    
def view_pdf(updrafts_file):
    ds = xr.open_dataset(updrafts_file); 
    CBU = ds.v
    binwidth = 0.5
    xr.plot.hist(CBU, bins=np.arange(CBU.min(), CBU.max() + binwidth, binwidth), density=True)
    plt.title(str(ds.time[0].values)[:10], loc='left')
    plt.title('Probability Density Function')
    
def view_kde(updrafts_file):
    ds = xr.open_dataset(updrafts_file); 
    df = ds.to_dataframe(); df.v
    sns.kdeplot(t.v)
    plt.title(str(ds.time[0].values)[:10], loc='left')
    plt.title('Kernel Density Estimation')
    
    
def plot_kde(updrafts_1, updrafts_2, updrafts_3):    
    
    
    files = [updrafts_1, updrafts_2, updrafts_3]
    
    for i in files:
        if fnmatch.fnmatch(i, '*updraft_1.nc'):
            ds1 = xr.open_dataset(i) 
        elif fnmatch.fnmatch(i, '*updraft_2.nc'):
            ds2 = xr.open_dataset(i)
        elif fnmatch.fnmatch(i, '*updraft_3.nc'):
            ds3 = xr.open_dataset(i)
    
    m1 = float(ds1.v.mean().values); m1 = round(m1,4)
    m2 = float(ds2.v.mean().values); m2 = round(m2,4)
    m3 = float(ds3.v.mean().values); m3 = round(m3,4)
    
    df1 = ds1.to_dataframe();
    df2 = ds2.to_dataframe();
    df3 = ds3.to_dataframe();
    
    fig, [ax1,ax2,ax3] = plt.subplots(ncols=3,sharey=True,sharex=True, tight_layout=True, figsize=(7, 3))
    
    sns.histplot(df1.v, binwidth=0.5, kde=True, stat="density", ax=ax1, color='grey', label=f'μ = {m1}')
    ax1.set_title('droplets, ice, drizzle')
    #ax1.set_xlabel('Doppler velocity (m/s)')
    sns.histplot(df2.v, binwidth=0.5, kde=True, stat="density", ax=ax2, color='#B276FF', label=f'μ = {m2}')
    ax2.set_title('droplets, drizzle')
    #ax2.set_xlabel('Doppler velocity (m/s)')
    sns.histplot(df3.v, binwidth=0.5, kde=True, stat="density", ax=ax3, color='#00D1FF', label=f'μ = {m3}')
    ax3.set_title('droplets')
    #ax3.set_xlabel('Doppler velocity (m/s)')
    
    for ax in [ax1,ax2,ax3]:
        ax.set_xlabel('Doppler velocity (m/s)')
        ax.legend(fontsize=8)
        
        
def plot_updrafts(classification_file, updraft_file): 
    
    classification = xr.open_dataset(classification_file)
    output_name = str(classification_file)
    site = output_name.split('_')[-2]
    classes, clouds, aerosols, insects, drizzle, ice, fog = get_classes(classification)
    CBU = xr.open_dataset(updraft_file) 
    
    assert str(CBU.time[0].values)[:10] == str(classification.time[0].values)[:10]
    
    fig, ax = plt.subplots(figsize=(9,3))
    y = CBU.v
    x = CBU.time
    z = drizzle
    f = fog

    maxlim = np.nanmax(CBU.v)

    z.values[z.values == 2.0] = -1.9
    z.values[z.values == 3.0] = -1.9
    f.values[f.values == 1.0] = -1.9

    x2 = drizzle.time
    x3 = fog.time

    plt.plot(x, y, color='#00D1FF', label='Vertical velocity', linestyle='None', marker=2)

    if np.count_nonzero(~np.isnan(drizzle)) == 0:
        pass
    else:
        plt.plot(x2, z, color='#B276FF', label='Drizzle flag', linestyle='None', marker='*')

    if np.count_nonzero(~np.isnan(fog)) == 0:
        pass
    else:
        plt.plot(x3, f, color='grey', label='Fog flag', linestyle='None', marker='*')

    ynew = 0
    ax.axhline(ynew, color='black')
    myFmt = mdates.DateFormatter('%H')
    ax.xaxis.set_major_formatter(myFmt)
    #for line in ax.get_lines(): # ax.lines:
    #  line.remove()
    plt.grid(axis='y', linestyle='-')
    plt.ylabel('Vertical Velocity (m/s)', fontsize=12) 
    plt.xlabel('Time (UTC)', fontsize=12) 
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper right', bbox_to_anchor=(.95,.95), prop={'size': 15})
    plt.ylim([-2, maxlim * 1.5])
    plt.title(site.capitalize() + ' ' + str(classification.time[0].values)[:10], loc='left')
    plt.title('Cloud Base Updrafts/Downdrafts', fontsize=14)

    plt.tight_layout()
    plt.show()