# --------------------------------------------------
# Registration of 2 MRI volumes using elastix. 
#
# - Roi version, using the inverse of the mask to register       
# - TODO New: 6/4/21 doing top and bottom registrations independently (top without mask, bottom with mask)
#
# Robert Marti 2021
# robert.marti@udg.edu
# 
# (fast2) robert@mariecurie:~/src/elastix$ python reg2volumes.py --non_rigid 0 --fixed_image /mnt/mia_images/wholebody/reg_ACF/ACF_26_221.nii.gz --moving_imag
# /mnt/mia_images/wholebody/reg_ACF/ACF_26_321.nii.gz --output_image ./affine_ACF_26_321.nii.gz --output_folder res_affine_mask/ 
# --fixed_mask  /mnt/mia_images/wholebody/reg_ACF/ACF_26_221_labels.nii.gz  
# --moving_mask  /mnt/mia_images/wholebody/reg_ACF/ACF_26_321_labels.nii.gz
# --------------------------------------------------

import os
import argparse
import time
import SimpleITK as sitk



CURRENT_FOLDER = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":

    # Parse input options
    parser = argparse.ArgumentParser(
        description="Volume registration using elastix- ROI version")
    parser.add_argument('--rig_aff_bsp',
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
    parser.add_argument('--output_folder',
                        action = 'store',
                        required=True,
                        help='output folder (mandatory)')

    parser.add_argument('--fixed_mask',
                        action = 'store',
                        required=False,
                        help='fixed_mask (optional)')

    parser.add_argument('--moving_mask',
                        action = 'store',
                        required=False,
                        help='moving_mask (optional)')
    
    
    opt = parser.parse_args()
    
    fixed_fn = opt.fixed_image
    moving_fn = opt.moving_image    
    output_fn = opt.output_image
    output_fd = opt.output_folder

    roi_version = True
    threshold_MRI = 35

    if (opt.fixed_mask is not None) and (opt.moving_mask is not None):
        moving_mask_fn = opt.moving_mask
        fixed_mask_fn = opt.fixed_mask
        using_masks = True
    else: using_masks = False

    rig_aff_bsp = opt.rig_aff_bsp
    print ("Files: ", fixed_fn, moving_fn,output_fn)
    print ("Transformation type (rigid/affine/bsplines): ",rig_aff_bsp)

    fixed_im = sitk.ReadImage(fixed_fn)
    moving_im = sitk.ReadImage(moving_fn)
    # set same origins & spacings
    f_org = fixed_im.GetOrigin()   
    m_org = moving_im.GetOrigin()
    f_sp = fixed_im.GetSpacing()
    m_sp = moving_im.GetSpacing()

    if (using_masks):
        fixed_msk = sitk.ReadImage(fixed_mask_fn)
        moving_msk = sitk.ReadImage(moving_mask_fn)
        fixed_msk.SetSpacing(f_sp)
        moving_msk.SetSpacing(m_sp)
        fixed_msk.SetOrigin(f_org)
        moving_msk.SetOrigin(m_org)
        # roi_version
        if roi_version: 
            # cropping Fixed 
            labels_stats = sitk.LabelStatisticsImageFilter()
            labels_stats.Execute(fixed_im, fixed_msk)
            bbox = labels_stats.GetBoundingBox(1) # label 0 is background CAUTION !returns [xstart, xend,  ystart, yend, z start, zend].
            print("Cropping bbox Fixed ",bbox)
            crop = sitk.CropImageFilter()
            # print(labels_stats.GetLabels()) #(Should print (0,1,2,3))
            crop.SetLowerBoundaryCropSize((bbox[0],bbox[2],bbox[4]))
            crop.SetUpperBoundaryCropSize((fixed_im.GetWidth()-bbox[1],fixed_im.GetHeight()-bbox[3],fixed_im.GetDepth()-bbox[5]))
            fixed_crop= crop.Execute(fixed_im)
            sitk.WriteImage(fixed_crop, output_fd+"fixed_cropped.nii.gz")                     
            fixed_mcrop = crop.Execute(fixed_msk)
            sitk.WriteImage(fixed_mcrop, output_fd+"fixed_m_cropped.nii.gz")

            # cropping Moving
            labels_stats.Execute(moving_im, moving_msk)
            bbox = labels_stats.GetBoundingBox(1) # label 0 is background CAUTION !returns [xstart, xend,  ystart, yend, z start, zend].
            print("Cropping bbox Moving ",bbox)
            crop.SetLowerBoundaryCropSize((bbox[0],bbox[2],bbox[4]))
            crop.SetUpperBoundaryCropSize((moving_im.GetWidth()-bbox[1],moving_im.GetHeight()-bbox[3],moving_im.GetDepth()-bbox[5]))
            moving_crop= crop.Execute(moving_im)
            sitk.WriteImage(moving_crop, output_fd+"moving_cropped.nii.gz")                     
            moving_mcrop = crop.Execute(moving_msk)
            sitk.WriteImage(moving_mcrop, output_fd+"moving_m_cropped.nii.gz")
            print("--> Cropping done")

            # now fixed and moving are the cropped ones
            fixed_im = fixed_crop
            moving_im = moving_crop
            fixed_msk = fixed_mcrop
            moving_msk = moving_mcrop
   
    print(fixed_im.GetPixelIDTypeAsString())
    fixed_pixelID = fixed_im.GetPixelID()

    # # fixed_im.SetOrigin (f_sp)
    # moving_im.SetOrigin (f_org)
    # moving_im.SetSpacing(f_sp)
    # moving_im.CopyInformation(fixed_im)
    moving_r_im = sitk.Resample(moving_im, fixed_im, sitk.Transform(), sitk.sitkNearestNeighbor, 0.0, fixed_im.GetPixelID())

        
    # diff_fm = sitk.AbsoluteValueDifference(fixed_im,moving_im)
    diff_fm = sitk.Subtract(fixed_im,moving_r_im)

    sitk.WriteImage(diff_fm, output_fd+"diff_before.nii.gz")

    # undo the modifications.
    # moving_im.SetOrigin (m_org)
    # moving_im.SetSpacing(m_sp)

    elastixImageFilter = sitk.ElastixImageFilter()
    elastixImageFilter.SetFixedImage(fixed_im)
    elastixImageFilter.SetMovingImage(moving_im)      
        
    parameterMapVector = sitk.VectorOfParameterMap()
    if (rig_aff_bsp == '0'):
        parameterMapVector.append(sitk.GetDefaultParameterMap("rigid"))
    if (rig_aff_bsp == '1'):
        parameterMapVector.append(sitk.GetDefaultParameterMap("affine"))    
    if (rig_aff_bsp == '2'):
        parameterMapVector.append(sitk.GetDefaultParameterMap("bspline"))


    elastixImageFilter.SetParameterMap(parameterMapVector)
    # elastixImageFilter.SetParameter("FinalGridSpacingInPhysicalUnits",'100')  #"50.0 50.0 50.0")#"8.0 8.0 8.0")  (FinalGridSpacingInPhysicalUnits 8)
    # elastixImageFilter.SetParameter("GridSpacingSchedule", ['4.0','2.0','1.0']) #  (GridSpacingSchedule 2.80322 1.9881 1.41 1)
    # elastixImageFilter.SetParameter("NumberOfResolutions", '3') #  (GridSpacingSchedule 2.80322 1.9881 1.41 1)
    if (rig_aff_bsp != '2'):
        elastixImageFilter.SetParameter("FinalGridSpacingInPhysicalUnits",'5')  #"50.0 50.0 50.0")#"8.0 8.0 8.0")  (FinalGridSpacingInPhysicalUnits 8)
        # elastixImageFilter.SetParameter("GridSpacingSchedule", ['8.0','4.0','2.0','1.0']) #  (GridSpacingSchedule 2.80322 1.9881 1.41 1)
        # elastixImageFilter.SetParameter("NumberOfResolutions", '4') #  (GridSpacingSchedule 2.80322 1.9881 1.41 1)
        elastixImageFilter.SetParameter("GridSpacingSchedule", ['8.0','4.0','2.0' '1.0']) #  (GridSpacingSchedule 2.80322 1.9881 1.41 1)
        elastixImageFilter.SetParameter("NumberOfResolutions", '4') #  (GridSpacingSchedule 2.80322 1.9881 1.41 1)
    elastixImageFilter.SetParameter("MaximumNumberOfIterations",'5000') # max number of iterations was 255
    elastixImageFilter.SetParameter("NumberOfSpatialSamples",'8192') # was 2048
    elastixImageFilter.SetOutputDirectory(output_fd)
    
    using_masks = True
    if (using_masks):
        print('using Masks')
        elastixImageFilter.SetFixedMask(fixed_msk)
        # Is better to only include fixed_mask (that's why is below commented) in case of small masks, to avoid not enough samples error!
        # elastixImageFilter.SetMovingMask(moving_msk)  
        elastixImageFilter.SetParameter("MaximumNumberOfSamplingAttempts",'500') # was 8 by default
        elastixImageFilter.SetParameter("RequiredRatioOfValidSamples",'0.25') #'0.01') # was 0.25  by default
        elastixImageFilter.SetParameter("ImageSampler",'RandomSparseMask') # was 0.25  by default
        elastixImageFilter.SetParameter("NumberOfSpatialSamples",'16384') #'8192') # was 2048    
    else: print('NOT using masks for reg')

    using_masks = True # for not using masks during reg         
    elastixImageFilter.PrintParameterMap()

    # input('press to execute')
    elastixImageFilter.Execute()  
   
    transf_moving = elastixImageFilter.GetResultImage()
    sitk.WriteImage(transf_moving, output_fd+output_fn)
     
    transformixImageFilter = sitk.TransformixImageFilter()
    transformixImageFilter.SetTransformParameterMap(elastixImageFilter.GetTransformParameterMap())
    transformixImageFilter.ComputeDeformationFieldOn()
    transformixImageFilter.LogToConsoleOn()
    transformixImageFilter.ComputeDeterminantOfSpatialJacobianOn()
    # transformixImageFilter.ComputeSpatialJacobianOn() no need for jacobian (too much space)
    transformixImageFilter.SetOutputDirectory(output_fd)
    transformixImageFilter.SetMovingImage(moving_im)
    transformixImageFilter.Execute()
    deformationField = transformixImageFilter.GetDeformationField()


    # print(fixed_im.GetPixelIDTypeAsString())
    # print(transf_moving.GetPixelIDTypeAsString())
    transf_moving_cast = sitk.Cast(transf_moving,fixed_pixelID)
   
    # diff_after = sitk.AbsoluteValueDifference(fixed_im,transf_moving_cast)
    diff_after = sitk.Subtract(fixed_im,transf_moving_cast)
    sitk.WriteImage(diff_after, output_fd+"diff_after.nii.gz")

    # transform the mask
    if (using_masks):
        print('Deforming mask')        
        transformixImageFilter.SetTransformParameter('FinalBSplineInterpolationOrder', '0')
        transformixImageFilter.SetMovingImage(moving_msk)
        transformixImageFilter.ComputeDeterminantOfSpatialJacobianOff()
        transformixImageFilter.Execute()
        transf_moving_msk = transformixImageFilter.GetResultImage()
        transf_moving_cast = sitk.Cast(transf_moving_msk,moving_msk.GetPixelID())
        transf_moving_cast = transf_moving_cast
        sitk.WriteImage(transf_moving_cast, output_fd+'transf_mask.nii.gz')



    
    
