# --------------------------------------------------
# Difference of 2 MRI volumes using elastix. 
#
#       
#
# Robert Marti 2021
# robert.marti@udg.edu
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
        description="Make a volume difference between images")
    parser.add_argument('--fixed_image',
                        action='store',
                        required=True,
                        help='Input FIXED volume file  (mandatory)')
    parser.add_argument('--moving_image',
                        action='store',
                        required=True,
                        help='Input MOVING volume file  (mandatory)')
    parser.add_argument('--output_image',
                        action = 'store',
                        required=True,
                        help='output transformed moving image filename (mandatory)')
    parser.add_argument('--offset',
                        action = 'store',
                        required=False,
                        help='offset value (int) to multiply moving_im (optiona)')
    
    opt = parser.parse_args()

    if (opt.offset) is None: offset = 1
    else: offset = opt.offset
    
    fixed_fn = opt.fixed_image
    moving_fn = opt.moving_image    
    output_fn = opt.output_image
    print ("Files: ", fixed_fn, moving_fn,output_fn,"offset:",offset)
    
    fixed_im = sitk.ReadImage(fixed_fn)
    moving_im = sitk.ReadImage(moving_fn)

    moving_im = moving_im*offset

    print(fixed_im.GetPixelIDTypeAsString())
    print(moving_im.GetPixelIDTypeAsString())
    
    moving_r_im = sitk.Resample(moving_im, fixed_im, sitk.Transform(), sitk.sitkNearestNeighbor, 0.0, fixed_im.GetPixelID())      
    diff_fm = sitk.Subtract(fixed_im,moving_r_im)

    sitk.WriteImage(diff_fm, output_fn)

    
    
