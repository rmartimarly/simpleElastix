# crop masks  

i_folder="/mnt/mia_images/wholebody/reg_MCM"
out_dir="crop_masks_MCM"
bl_vol="MCM_baseline"
t1_vol="MCM_30_221"
t2_vol="MCM_30_321"


mkdir ${out_dir}

python crop_volume.py  --input_image ${i_folder}/${bl_vol}_labels.nii.gz --axis z --keep 0 --output_image ${out_dir}/${bl_vol}-labels_z0.nii.gz

python crop_volume.py  --input_image ${i_folder}/${bl_vol}_labels.nii.gz --axis z --keep 1 --output_image ${out_dir}/${bl_vol}-labels_z1.nii.gz

python crop_volume.py  --input_image ${i_folder}/${t1_vol}_labels.nii.gz --axis z --keep 0 --output_image ${out_dir}/${t1_vol}-labels_z0.nii.gz

python crop_volume.py  --input_image ${i_folder}/${t1_vol}_labels.nii.gz --axis z --keep 1 --output_image ${out_dir}/${t1_vol}-labels_z1.nii.gz

python crop_volume.py  --input_image ${i_folder}/${t2_vol}_labels.nii.gz --axis z --keep 0 --output_image ${out_dir}/${t2_vol}-labels_z0.nii.gz

python crop_volume.py  --input_image ${i_folder}/${t2_vol}_labels.nii.gz --axis z --keep 1 --output_image ${out_dir}/${t2_vol}-labels_z1.nii.gz


