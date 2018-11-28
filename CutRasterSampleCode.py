#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 10:11:27 2018

@author: steve
"""

import rasterio

rasterfileMulti = 'MOD10A1_multiband_HEGOUT.hdf'
rasterfileSingle = 'MOD10A1_singleband_HEGOUT.hdf'
shapeFile = 'SFP_drainage.shp'


# =============================================================================
# Read an HDF with only one band or dataset into an array.
# This works as expected.
# =============================================================================
dataset = rasterio.open('rasterfileSingle')
print(dataset.indexes)
band1 = dataset.read(1)
print(band1)


# =============================================================================
# Read an HDF with only one band or dataset into an array.
# This does not work becaus eI don't understand how to
# open the dataset (or band) called NDSI_Snow_Ccover.
# =============================================================================
dataset2 = rasterio.open('rasterfileMulti')
print(dataset2.indexes)
band1 = dataset.read(1)
print(band1)




# =============================================================================
# Ultimatley, this is what I am trying to accomplish. The code below works
# for an HDF with one band but not for an HDF containing multiple bands.
# I'm only intrested in the NDSI_Snow_Cover dataset.
# =============================================================================

import fiona
import rasterio


with fiona.open(shapeFile, 'r') as shapefile:
    features = [feature['geometry'] for feature in shapefile]
    
   
with rasterio.open(rasterfileMulti) as src:
    out_image, out_transform = rasterio.mask.mask(src, features,
                                                        crop=True)
    out_meta = src.meta.copy()
    

out_meta.update({'driver': 'GTiff',
                 'height': out_image.shape[1],
                 'width': out_image.shape[2],
                 'transform': out_transform})
with rasterio.open('/Users/steve/Documents/classes/Geos_505/project_Payette/working/data_files/test_clip_out.tif', 'w', **out_meta) as dest:
    dest.write(out_image)