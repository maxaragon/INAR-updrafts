from datetime import datetime 
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

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

def plot_all(first=None, second=None, third=None, title=None):
    fig, (ax1) = plt.subplots(1, figsize=(12, 4), sharey=True, sharex=True)
    myFmt = mdates.DateFormatter('%H')

    for ax in [ax1]:
      ax.xaxis.set_major_formatter(myFmt)


    if first is None:
        pass
    else:
        if 1 in np.unique(first.values[~np.isnan(first.values)]):
          cmap = mpl.colors.ListedColormap(['b'])
          first.plot(x='time', ax=ax1, add_colorbar=False, cmap=cmap)
        elif 2 in np.unique(first.values[~np.isnan(first.values)]):
          cmap = mpl.colors.ListedColormap(['g'])
          first.plot(x='time', ax=ax1, add_colorbar=False, cmap=cmap)
        elif 4 in np.unique(first.values[~np.isnan(first.values)]):
          cmap = mpl.colors.ListedColormap(['y'])
          first.plot(x='time', ax=ax1, add_colorbar=False, cmap=cmap)
        elif 9 in np.unique(first.values[~np.isnan(first.values)]):
          cmap = mpl.colors.ListedColormap(['r'])
          first.plot(x='time', ax=ax1, add_colorbar=False, cmap=cmap)  
    
    if second is None:
        pass
    else:
        if 1 in np.unique(second.values[~np.isnan(second.values)]):
          cmap = mpl.colors.ListedColormap(['b'])
          second.plot(x='time', ax=ax1, add_colorbar=False, cmap=cmap)
        elif 2 in np.unique(second.values[~np.isnan(second.values)]):
          cmap = mpl.colors.ListedColormap(['g'])
          second.plot(x='time', ax=ax1, add_colorbar=False, cmap=cmap)
        elif 4 in np.unique(second.values[~np.isnan(second.values)]):
          cmap = mpl.colors.ListedColormap(['y'])
          second.plot(x='time', ax=ax1, add_colorbar=False, cmap=cmap)
        elif 9 in np.unique(second.values[~np.isnan(second.values)]):
          cmap = mpl.colors.ListedColormap(['r'])
          second.plot(x='time', ax=ax1, add_colorbar=False, cmap=cmap)
      


    if third is None:
        pass
    else:
        if 1 in np.unique(third.values[~np.isnan(third.values)]):
          cmap = mpl.colors.ListedColormap(['b'])
          third.plot(x='time', ax=ax1, add_colorbar=False, cmap=cmap)
        elif 2 in np.unique(third.values[~np.isnan(third.values)]):
          cmap = mpl.colors.ListedColormap(['g'])
          third.plot(x='time', ax=ax1, add_colorbar=False, cmap=cmap)
        elif 4 in np.unique(third.values[~np.isnan(third.values)]):
          cmap = mpl.colors.ListedColormap(['y'])
          third.plot(x='time', ax=ax1, add_colorbar=False, cmap=cmap)
        elif 9 in np.unique(third.values[~np.isnan(third.values)]):
          cmap = mpl.colors.ListedColormap(['r'])
          third.plot(x='time', ax=ax1, add_colorbar=False, cmap=cmap)
        

    for ax in [ax1]:
      ax.set_ylim([0, np.nanmax(first.height) + 300])
      ax.set_xlim([startx(classes), endx(classes)])
      ax.set_title(str(classification.time[0].values)[:10], loc='left')
      ax.set_title(title)
      #ax.legend()
    for label in ax.get_xticklabels():
      label.set_rotation(0);
    
    
def view_pdf(updrafts_file):
    ds = xr.open_dataset(updrafts_file); 
    CBU = ds.v
    binwidth = 0.5
    xr.plot.hist(CBU, bins=np.arange(CBU.min(), CBU.max() + binwidth, binwidth), density=True)
    plt.title(str(ds.time[0].values)[:10], loc='left')
    plt.title('Probability Density Function')