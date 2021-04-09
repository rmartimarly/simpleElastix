# first registration of MCM (baseline agains first time point
# doing rigid registration, using ROI (cropping image) and registration with mask.

i_folder="/mnt/mia_images/wholebody/reg_ACF"
out_dir="ACF_reg2_rigid_rm_z0"
f_vol="acf_26_baseline"
m_vol="ACF_26_321"

mkdir ${out_dir}

python reg2volumes_roi.py --rig_aff_bsp 0 --fixed_image ${i_folder}/${f_vol}.nii.gz --moving_image ${i_folder}/${m_vol}.nii.gz --output_image ./rigid_roi_mask_${m_vol}.nii.gz --output_folder ${out_dir}/ --fixed_mask  ${i_folder}/${f_vol}_labels_z0.nii.gz --moving_mask  ${i_folder}/${m_vol}_labels_z0.nii.gz

python diff_images.py --fixed_image ${out_dir}/fixed_m_cropped.nii.gz  --moving_image ${out_dir}/transf_mask.nii.gz  --output_image ${out_dir}/mask_diff255.nii.gz --offset 10

python mask_volume.py --input_image ${out_dir}/fixed_cropped.nii.gz  --mask_image ${out_dir}/fixed_m_cropped.nii.gz  --output_image ${out_dir}/fixed_cropped_masked.nii.gz
python mask_volume.py --input_image ${out_dir}/moving_cropped.nii.gz  --mask_image ${out_dir}/moving_m_cropped.nii.gz  --output_image ${out_dir}/moving_cropped_masked.nii.gz

