# --------------------------------------------------
# Crop half of the a volume
#
# - Input: volume and axis
# - Outoput: cropped volume. 
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
    parser.add_argument('--axis',
                        action='store',
                        required=True,
                        help='Axis to crop (mandatory)')
    parser.add_argument('--keep',
                        action='store',
                        required=True,
                        help='half to keep (0/1)')                        
    parser.add_argument('--output_image',
                        action = 'store',
                        required=True,
                        help='output cropped volume filename (mandatory)')
    
    opt = parser.parse_args()
    
    input_im = opt.input_image
    axis = opt.axis 
    keep = opt.keep
    output_fn = opt.output_image
    print ("Files: ", input_im , axis, keep,output_fn)
    
    input_im = sitk.ReadImage(input_im)
    
    print(input_im.GetPixelIDTypeAsString())

    dx = input_im.GetWidth()
    dy = input_im.GetHeight()
    dz = input_im.GetDepth()
  
    crop = sitk.CropImageFilter()    
    lower = (0, 0, 0)    
    if (axis=='x'): # cut in width
        upper = (dx-int(dx/2),0,0)
    elif (axis=='y'):
        upper = (0,dy-int(dy/2),0)
    elif (axis=='z'):
        upper = (0,0,dz-int(dz/2))
    else: print("Wrong axis (should be x,y,z). Not cropping")
    
    if (keep=='1'):
        upper = (0,0,0)
        if (axis=='x'): # cut in width
            lower = (int(dx/2),0,0)
        elif (axis=='y'):
            lower = (0,int(dy/2),0)
        elif (axis=='z'):
            lower = (0,0,int(dz/2))
        else: print("Wrong axis (should be x,y,z). Not cropping")

    print(dx,dy,dz, "lower", lower, "upper",upper)
    crop.SetLowerBoundaryCropSize(lower)
    crop.SetUpperBoundaryCropSize(upper)
    input_cropped = crop.Execute(input_im)
    sitk.WriteImage(input_cropped, output_fn)
    dx = input_cropped.GetWidth()
    dy = input_cropped.GetHeight()
    dz = input_cropped.GetDepth()
    print("new dim:",dx,dy,dz)
    


