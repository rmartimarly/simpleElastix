# --------------------------------------------------
# Registration of 2 MRI volumes using elastix. 
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
        description="Volume registration using elastix")
    parser.add_argument('--non_rigid',
                        action='store',
                        required=True,
                        help='Perform (1) or not (0) non-rigid registration (mandatory)')
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
    
    opt = parser.parse_args()
    
    fixed_fn = opt.fixed_image
    moving_fn = opt.moving_image    
    output_fn = opt.output_image
    if (opt.non_rigid == '1'): do_non_rigid = True
    else: do_non_rigid = False
    print ("Files: ", fixed_fn, moving_fn,output_fn)
    print ("Doing non-rigid: ",do_non_rigid)

    moving_im = sitk.ReadImage(moving_fn)
    fixed_im = sitk.ReadImage(fixed_fn)

    print(fixed_im.GetPixelIDTypeAsString())
    fixed_pixelID = fixed_im.GetPixelID()


    # set same origins
    f_org = fixed_im.GetOrigin()   
    m_org = moving_im.GetOrigin()
    f_sp = fixed_im.GetSpacing()
    m_sp = moving_im.GetSpacing()

    # fixed_im.SetOrigin (f_sp)
    moving_im.SetOrigin (f_org)
    moving_im.SetSpacing(f_sp)
    
    # diff_fm = sitk.AbsoluteValueDifference(fixed_im,moving_im)
    diff_fm = sitk.Subtract(fixed_im,moving_im)

    sitk.WriteImage(diff_fm, "diff_before.nii.gz")

    # undo the modifications.
    moving_im.SetOrigin (m_org)
    moving_im.SetSpacing(m_sp)

    elastixImageFilter = sitk.ElastixImageFilter()
    elastixImageFilter.SetFixedImage(fixed_im)
    elastixImageFilter.SetMovingImage(moving_im)

    parameterMapVector = sitk.VectorOfParameterMap()
    parameterMapVector.append(sitk.GetDefaultParameterMap("affine"))
    if (do_non_rigid):
        parameterMapVector.append(sitk.GetDefaultParameterMap("bspline"))


    elastixImageFilter.SetParameterMap(parameterMapVector)
    # elastixImageFilter.SetParameter("FinalGridSpacingInPhysicalUnits",'100')  #"50.0 50.0 50.0")#"8.0 8.0 8.0")  (FinalGridSpacingInPhysicalUnits 8)
    # elastixImageFilter.SetParameter("GridSpacingSchedule", ['4.0','2.0','1.0']) #  (GridSpacingSchedule 2.80322 1.9881 1.41 1)
    # elastixImageFilter.SetParameter("NumberOfResolutions", '3') #  (GridSpacingSchedule 2.80322 1.9881 1.41 1)
    if (do_non_rigid): 
        elastixImageFilter.SetParameter("FinalGridSpacingInPhysicalUnits",'5')  #"50.0 50.0 50.0")#"8.0 8.0 8.0")  (FinalGridSpacingInPhysicalUnits 8)
        elastixImageFilter.SetParameter("GridSpacingSchedule", ['8.0','4.0','2.0','1.0']) #  (GridSpacingSchedule 2.80322 1.9881 1.41 1)
        elastixImageFilter.SetParameter("NumberOfResolutions", '4') #  (GridSpacingSchedule 2.80322 1.9881 1.41 1)
    elastixImageFilter.SetParameter("MaximumNumberOfIterations",'500') # max number of iterations was 255

    elastixImageFilter.PrintParameterMap()
    input('press to execute')
    elastixImageFilter.Execute()  
   
    transf_moving = elastixImageFilter.GetResultImage()
    sitk.WriteImage(transf_moving, output_fn)
     
    transformixImageFilter = sitk.TransformixImageFilter()
    transformixImageFilter.SetTransformParameterMap(elastixImageFilter.GetTransformParameterMap())
    transformixImageFilter.ComputeDeformationFieldOn()
    transformixImageFilter.LogToConsoleOn()
    transformixImageFilter.ComputeDeformationFieldOn()
    transformixImageFilter.ComputeDeterminantOfSpatialJacobianOn()
    transformixImageFilter.ComputeSpatialJacobianOn()
    transformixImageFilter.SetOutputDirectory("./deform_output")
    transformixImageFilter.SetMovingImage(moving_im)
    transformixImageFilter.Execute()
    deformationField = transformixImageFilter.GetDeformationField()


    # print(fixed_im.GetPixelIDTypeAsString())
    # print(transf_moving.GetPixelIDTypeAsString())
    transf_moving_cast = sitk.Cast(transf_moving,fixed_pixelID)
   
    # diff_after = sitk.AbsoluteValueDifference(fixed_im,transf_moving_cast)
    diff_after = sitk.Subtract(fixed_im,transf_moving_cast)
    sitk.WriteImage(diff_after, "diff_after.nii.gz")

    
    
