# crop masks  

i_folder="/mnt/mia_images/wholebody/reg_ACF"
out_dir="crop_masks"
bl_vol="acf_26_baseline"
t1_vol="ACF_26_221"
t2_vol="ACF_26_321"


mkdir ${out_dir}

python crop_volume.py  --input_image ${i_folder}/${bl_vol}_labels.nii.gz --axis z --keep 0 --output_image ${out_dir}/${bl_vol}-labels_z0.nii.gz

python crop_volume.py  --input_image ${i_folder}/${bl_vol}_labels.nii.gz --axis z --keep 1 --output_image ${out_dir}/${bl_vol}-labels_z1.nii.gz

python crop_volume.py  --input_image ${i_folder}/${t1_vol}_labels.nii.gz --axis z --keep 0 --output_image ${out_dir}/${t1_vol}-labels_z0.nii.gz

python crop_volume.py  --input_image ${i_folder}/${t1_vol}_labels.nii.gz --axis z --keep 1 --output_image ${out_dir}/${t1_vol}-labels_z1.nii.gz

python crop_volume.py  --input_image ${i_folder}/${t2_vol}_labels.nii.gz --axis z --keep 0 --output_image ${out_dir}/${t2_vol}-labels_z0.nii.gz

python crop_volume.py  --input_image ${i_folder}/${t2_vol}_labels.nii.gz --axis z --keep 1 --output_image ${out_dir}/${t2_vol}-labels_z1.nii.gz


