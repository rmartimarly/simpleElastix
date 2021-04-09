# --------------------------------------------------
# Mask a volume given an input mask
#
# - Input: volume and mask
# - Outoput: masked volume. 
#
# Robert Marti 2021
# robert.marti@udg.edu
#   TODO: https://simpleitk.org/doxygen/latest/html/classitk_1_1simple_1_1MaskImageFilter.html
# 
# --------------------------------------------------


import os
import argparse
import time
import SimpleITK as sitk

CURRENT_FOLDER = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":

    # Parse input options
    parser = argparse.ArgumentParser(
        description="Mask a volume using input mask")
    parser.add_argument('--input_image',
                        action='store',
                        required=True,
                        help='Input volume file  (mandatory)')
    parser.add_argument('--mask_image',
                        action='store',
                        required=True,
                        help='Input mask volume file  (mandatory)')
    parser.add_argument('--output_image',
                        action = 'store',
                        required=True,
                        help='output masked volume filename (mandatory)')
    
    opt = parser.parse_args()
    
    input_im = opt.input_image
    mask_im = opt.mask_image    
    output_fn = opt.output_image
    print ("Files: ", input_im , mask_im,output_fn)
    
    input_im = sitk.ReadImage(input_im)
    mask_im = sitk.ReadImage(mask_im)

    print(input_im.GetPixelIDTypeAsString())

    i_org = input_im.GetOrigin()   
    i_sp = input_im.GetSpacing()
    
    mask_im.SetSpacing(i_sp)
    mask_im.SetOrigin(i_org)

    #mask_im = (mask_im==1) #removed assume they have different values. 
    
    mask_im_r = sitk.Resample(mask_im, input_im, sitk.Transform(), sitk.sitkNearestNeighbor, 0.0, mask_im.GetPixelID())
    
    mask_filter = sitk.MaskImageFilter()
    masked_image = mask_filter.Execute(input_im,mask_im_r)

    sitk.WriteImage(masked_image, output_fn)

