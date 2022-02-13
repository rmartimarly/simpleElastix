# --------------------------------------------------
# Crop half of the a volume
#
# - Input: volume and axis
# - Outoput: cropped volume. 
# - CUSTOM: cuts the axis in NC cuts and keeps 3-4
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
import numpy as np

CURRENT_FOLDER = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":

    # Parse input options
    parser = argparse.ArgumentParser(
        description="Put to 0 half of a volume of an image given an axis")
    parser.add_argument('--input_image',
                        action='store',
                        required=True,
                        help='Input volume file  (mandatory)')
    parser.add_argument('--axis',
                        action='store',
                        required=True,
                        help='Axis to crop (mandatory)')
    parser.add_argument('--n_cuts',
                        action='store',
                        required=True,
                        help='Number of cuts')                        
    parser.add_argument('--start_cut',
                        action='store',
                        required=True,
                        help='starting cut')                        
    parser.add_argument('--end_cut',
                        action='store',
                        required=True,
                        help='starting cut')                                            
    parser.add_argument('--output_image',
                        action = 'store',
                        required=True,
                        help='output cropped volume filename (mandatory)')
    
    opt = parser.parse_args()
    
    input_im = opt.input_image
    axis = opt.axis 
    output_fn = opt.output_image
    n_cuts = int(opt.n_cuts) #5 # number of cuts.
    s_cut = int(opt.start_cut) #3 # starting cut (0 is first cut)
    e_cut = int(opt.end_cut) # 4 # end _cut not included.
    print ("Files: ", input_im , axis, n_cuts, s_cut, e_cut,output_fn)
    
    input_im = sitk.ReadImage(input_im)
    
    print(input_im.GetPixelIDTypeAsString())

    dx = input_im.GetWidth()-1
    dy = input_im.GetHeight()-1
    dz = input_im.GetDepth()-1

 
    cut_sx = (dx/n_cuts) # cut size in x
    cut_sy = (dy/n_cuts) # cut size in y
    cut_sz = (dz/n_cuts) # cut size in z

    sx = 0
    sy = 0
    sz = 0
    ex = dx
    ey = dy
    ez = dz

    if (axis=='x'): # cut in width
        # ex = int(ex/2)
        sx = int(s_cut * cut_sx)
        ex = int((e_cut * cut_sx))
    elif (axis=='y'):
        sy = int(s_cut * cut_sy)
        ey = int((e_cut * cut_sy))
    elif (axis=='z'):
        sz = int(s_cut * cut_sz)
        ez = int((e_cut * cut_sz))
    else: print("Wrong axis (should be x,y,z). Not cropping")
    
    # if (keep=='0'):
    #     if (axis=='x'): # cut in width
    #         sx = ex
    #     elif (axis=='y'):
    #         sy = ey
    #     elif (axis=='z'):
    #         sz = ez
    #     else: print("Wrong axis (should be x,y,z). Not cropping")
    #     ex = dx
    #     ey = dy
    #     ez = dz
    print("Org dims: ",dx, dy, dz)
    # print(input_im.GetSize())
    print("blank info",sx, ex, sy, ey, sz, ez)
    # input_im[sx:ex,sy:ey,sz:ez] = 0
    nda = sitk.GetArrayFromImage(input_im)
    nda2 = sitk.GetArrayFromImage(input_im)
    nda2 [:,:,:] = 0
    nda2 [sz:ez,sy:ey,sx:ex] = nda [sz:ez,sy:ey,sx:ex]  
    img = sitk.GetImageFromArray(nda2)
    img.SetOrigin(input_im.GetOrigin())
    img.SetSpacing(input_im.GetSpacing())
    img.SetDirection(input_im.GetDirection())
# new_sitk_image.SetSpacing(tuple(itk_image.GetSpacing()))
# new_sitk_image.SetDirection(itk.GetArrayFromMatrix(itk_image.GetDirection()).flatten()) 
    # print(img.GetSize())
    sitk.WriteImage(img, output_fn)
  

    


