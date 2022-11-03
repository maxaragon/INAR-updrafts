import os
from gliders import *
from gliders.utils import download_cloudnet, get_classes, is_cloudnetpy_dir, is_cloudnetpy_file, open_files, preprocess
from gliders.filter import filter_drizzle_ice

# 1. Download classification and categorize data from Hyytiala

download_cloudnet(
    site='hyytiala', 
    start='2022-08-23', 
    end='2022-08-30', 
    output_dir=r'Products')


#1.5 Products location

classification_path = '/content/drive/MyDrive/INAR/Products/Classification'
categorize_path = '/content/drive/MyDrive/INAR/Products/Categorize'

# 2. Verify data in dirs is in CloudnetPy format else convert

is_cloudnetpy_dir(
    site='hyytiala',
    categorize_dir=r'Products/Categorize',
    classification_dir=r'Products/Classification')

# 2. Verify single files are in CloudnetPy format else convert

for classification, categorize in zip(os.listdir(classification_path), os.listdir(categorize_path)):
  is_cloudnetpy_file(os.path.join(classification_path, classification), os.path.join(categorize_path, categorize))

# 3. Open files

open_files(
    classification_file='Products/Classification/20140824_hyytiala_classification.nc',
     categorize_file='Products/Categorize/20140824_hyytiala_categorize.nc'
)

# 4. Get subset of classes (e.g. Liquid clouds, ice clouds, drizzle, etc)

get_classes(
    classification='', 
    categorize='')

# 5. Filter data (i.e. drizzle near cbh, insects near cbh, liquid clouds near ice) (filter.py)



# 6. View filters (plot.py)

view_filters(
    classification='', 
    categorize='')


# 7. Estimate cloud base updraft (CBU) (updraft.py)

generate_cbu(
    classification='', 
    categorize='')

# 8. View updrafts (plot.py)

view_cbu(
    classification='', 
    categorize='')


# 9. Get probability density function (updraft.py)

# 10 View PDF (plot.py)


updraft( 
    classification='', 
    categorize='',
    [original, processed, cbu, pdf_original, pdf_no_drizzle, pdf_no_drizzle_no_ice])