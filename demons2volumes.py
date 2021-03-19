# --------------------------------------------------
# Registration of 2 MRI volumes using elastix. 
#
#       
#
# Robert Marti 2021
# robert.marti@udg.edu
#  TODO: make it multiressolution: http://insightsoftwareconsortium.github.io/SimpleITK-Notebooks/Python_html/66_Registration_Demons.html
# --------------------------------------------------

import os
import argparse
import time
import SimpleITK as sitk


def command_iteration(filter):
    print(f"{filter.GetElapsedIterations():3} = {filter.GetMetric():10.5f}")


CURRENT_FOLDER = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":

    # Parse input options
    parser = argparse.ArgumentParser(
        description="Volume registration using elastix")
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
    print ("Files: ", fixed_fn, moving_fn,output_fn)

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
    
    diff_fm = sitk.AbsoluteValueDifference(fixed_im,moving_im)
    sitk.WriteImage(diff_fm, "diff_before.nii.gz")

    # undo the modifications.
    moving_im.SetOrigin (m_org)
    moving_im.SetSpacing(m_sp)

    # elastixImageFilter = sitk.ElastixImageFilter()
    # elastixImageFilter.SetFixedImage(fixed_im)
    # elastixImageFilter.SetMovingImage(moving_im)

    # parameterMapVector = sitk.VectorOfParameterMap()
    # parameterMapVector.append(sitk.GetDefaultParameterMap("affine"))
    # parameterMapVector.append(sitk.GetDefaultParameterMap("bspline"))


    # p=sitk.ParameterMap()

    
    # elastixImageFilter.SetParameterMap(parameterMapVector)
    # # elastixImageFilter.SetParameter("FinalGridSpacingInPhysicalUnits",'100')  #"50.0 50.0 50.0")#"8.0 8.0 8.0")  (FinalGridSpacingInPhysicalUnits 8)
    # # elastixImageFilter.SetParameter("GridSpacingSchedule", ['4.0','2.0','1.0']) #  (GridSpacingSchedule 2.80322 1.9881 1.41 1)
    # # elastixImageFilter.SetParameter("NumberOfResolutions", '3') #  (GridSpacingSchedule 2.80322 1.9881 1.41 1)
    # elastixImageFilter.SetParameter("FinalGridSpacingInPhysicalUnits",'5')  #"50.0 50.0 50.0")#"8.0 8.0 8.0")  (FinalGridSpacingInPhysicalUnits 8)
    # elastixImageFilter.SetParameter("GridSpacingSchedule", ['8.0','4.0','2.0','1.0']) #  (GridSpacingSchedule 2.80322 1.9881 1.41 1)
    # elastixImageFilter.SetParameter("NumberOfResolutions", '4') #  (GridSpacingSchedule 2.80322 1.9881 1.41 1)
    # elastixImageFilter.SetParameter("MaximumNumberOfIterations",'5000') # max number of iterations was 255


    # elastixImageFilter.PrintParameterMap()
    # input('press to execute')
    # elastixImageFilter.Execute()

    matcher = sitk.HistogramMatchingImageFilter()
    matcher.SetNumberOfHistogramLevels(1024)
    matcher.SetNumberOfMatchPoints(7)
    matcher.ThresholdAtMeanIntensityOn()
    moving_im = matcher.Execute(moving_im, fixed_im)

    # The basic Demons Registration Filter
    # Note there is a whole family of Demons Registration algorithms included in
    # SimpleITK
    # FastSymmetricForcesDemonsRegistrationFilter  DemonsRegistrationFilter
    demons = sitk.DemonsRegistrationFilter()
    
    demons.SetNumberOfIterations(500)
    # Standard deviation for Gaussian smoothing of displacement field
    demons.SetStandardDeviations(1.0)

    demons.AddCommand(sitk.sitkIterationEvent, lambda: command_iteration(demons))

    displacementField = demons.Execute(fixed_im, moving_im)

    print("-------")
    print(f"Number Of Iterations: {demons.GetElapsedIterations()}")
    print(f" RMS: {demons.GetRMSChange()}")


    outTx = sitk.DisplacementFieldTransform(displacementField)
    # print(displacementField)

    df_transf = sitk.DisplacementFieldTransform(outTx)
    disp_field = df_transf.GetDisplacementField()
    # print("end diuspl",disp_field)

    # df_transf = sitk.DisplacementFieldTransform(outTx)
    # deformation_field = df_transf.GetDisplacementField()
    print("Writing Deformation field...")
    sitk.WriteImage(disp_field,"demons_deformation.nii.gz")
    print("Writing Jacobian... ")
    jacobian = sitk.DisplacementFieldJacobianDeterminant(disp_field)
    sitk.WriteImage(jacobian,"demons_jacobian.nii.gz")  

    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(fixed_im)
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetDefaultPixelValue(100)
    resampler.SetTransform(outTx)

    transf_moving = resampler.Execute(moving_im)
    sitk.WriteImage(transf_moving, output_fn)

    sitk.WriteTransform(outTx,"out_trans.txt");
    transf_moving_cast = sitk.Cast(transf_moving,fixed_pixelID)
   
    diff_after = sitk.AbsoluteValueDifference(fixed_im,transf_moving_cast)
    sitk.WriteImage(diff_after, "demons_diff_after.nii.gz")

