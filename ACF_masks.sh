# first registration of MCM (baseline agains first time point
# doing rigid registration, using ROI (cropping image) and registration with mask.
in_dir="/mnt/mia_images/wholebody/reg_ACF"
out_dir="ACF_masks"
bl_vol="ACF_26_021"
t1_vol="ACF_26_221"
t2_vol="ACF_26_321"

mkdir ${out_dir}

python mask_volume.py --input_image ${in_dir}/acf_26_baseline.nii.gz  --mask_image  ${in_dir}/${bl_vol}-labels.nii  --output_image ${out_dir}/${bl_vol}_masked.nii.gz

python mask_volume.py --input_image ${in_dir}/${t1_vol}.nii.gz  --mask_image  ${in_dir}/${t1_vol}_labels.nii.gz  --output_image ${out_dir}/${t1_vol}_masked.nii.gz

python mask_volume.py --input_image ${in_dir}/${t2_vol}.nii.gz  --mask_image  ${in_dir}/${t2_vol}_labels.nii.gz  --output_image ${out_dir}/${t2_vol}_masked.nii.gz

