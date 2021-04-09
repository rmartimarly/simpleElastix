# first registration of MCM (baseline agains first time point
# doing rigid registration, using ROI (cropping image) and registration with mask.
in_dir="/mnt/mia_images/wholebody/reg_MCM"
out_dir="MCM_masks"
bl_vol="MCM_baseline"
t1_vol="MCM_30_221"
t2_vol="MCM_30_321"

mkdir ${out_dir}

python mask_volume.py --input_image ${in_dir}/${bl_vol}.nii.gz  --mask_image  ${in_dir}/${bl_vol}_labels.nii.gz  --output_image ${out_dir}/${bl_vol}_masked.nii.gz

python mask_volume.py --input_image ${in_dir}/${t1_vol}.nii.gz  --mask_image  ${in_dir}/${t1_vol}_labels.nii.gz  --output_image ${out_dir}/${t1_vol}_masked.nii.gz

python mask_volume.py --input_image ${in_dir}/${t2_vol}.nii.gz  --mask_image  ${in_dir}/${t2_vol}_labels.nii.gz  --output_image ${out_dir}/${t2_vol}_masked.nii.gz

