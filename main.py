import nibabel as nib
import os
from PIL import Image
import shutil
import numpy as np


INPUT_DIR = "/research/projects/BrainAbscess/mr_notion_february/nifti"
OUTPUT_DIR = INPUT_DIR.replace("mr_notion_february/nifti", "Sorted")

shutil.rmtree(OUTPUT_DIR)
logfile = open(os.path.join(OUTPUT_DIR, 'log.txt'), "w")

Patient_List = sorted(os.listdir(INPUT_DIR))

logfile.write('Original_Filename, Guessed_Name\n')

def mycopy(srcfile, tgdir, patient, type):
    # copy scrfile to tgdir/tgname
    # and write a PNG of central slice to that tgdir/PNG
    outfname = os.path.join(os.path.join(tgdir, patient), type)
    shutil.copy(srcfile, outfname)  # copy the nifti file

    # now make a PNG file for quick QC
    img = nib.load(srcfile)
    data_array = img.get_fdata()
    dims = img.shape
    xd = dims[0]
    yd = dims[1]
    zd = dims[2]
    axial_image = data_array[:, :, zd//2]  #
    min_val = np.percentile(axial_image, 5)
    max_val = np.percentile(axial_image, 95)
    img = axial_image * (255.0 / (max_val - min_val)) # scale to 0 - 255
    img = img.clip(0, 255)
    im = Image.fromarray(np.uint8(img))
    im = im.convert("L")  # or 'RGB'
    # first change name if .gz is in it
    if '.gz' in outfname:
        pname = outfname.replace(".nii.gz", ".png")
    else:
        pname = outfname.replace(".nii", ".png")
    im.save(pname)
    return outfname


for patient in Patient_List:
    Pre=None
    T2=None
    Post=None
    FLAIR=None
    ADC=None
    for series_dir in sorted(os.listdir(os.path.join(INPUT_DIR, patient))):
        dirname = os.path.join(os.path.join(INPUT_DIR, patient), series_dir).upper()
        if os.path.isdir(dirname):
            if 'FLAIR' in dirname and not 'T1' in dirname:
                FLAIR = True
            if 'T2' in dirname and not FLAIR:
                T2 = True
            if 'POST' in dirname or 'GD' in dirname or 'GAD' in dirname or 'WITH' in dirname:
                Post = True
            if 'PRE' in dirname or 'T1' in dirname:
                if not Post:
                    Pre = True
            if 'ADC' in dirname or 'APPARENT DIFF' in dirname:
                ADC=True
            # now need to find the nii file in the folder
            folder_list = os.listdir(dirname)
            fullname = None
            Guessed_Name = ''
            for f in folder_list:
                if '.NII' in f.upper():
                    fullname = os.path.join(dirname, f)
            if fullname is not None:
                if FLAIR:
                    if '.GZ' in fullname.upper():
                        Guessed_Name = mycopy(fullname, OUTPUT_DIR, patient, 'FLAIR.nii.gz')
                    else:
                        Guessed_Name = mycopy(fullname, OUTPUT_DIR, patient, 'FLAIR.nii')
                if T2:
                    if '.GZ' in fullname.upper():
                        Guessed_Name = mycopy(fullname, OUTPUT_DIR, patient, 'T2.nii.gz')
                    else:
                        Guessed_Name = mycopy(fullname, OUTPUT_DIR, patient, 'T2.nii')
                if Post:
                    if '.GZ' in fullname.upper():
                        Guessed_Name = mycopy(fullname, OUTPUT_DIR, patient, 'Post.nii.gz')
                    else:
                        Guessed_Name = mycopy(fullname, OUTPUT_DIR, patient, 'Post.nii')
                if Pre:
                    if '.GZ' in fullname.upper():
                        Guessed_Name = mycopy(fullname, OUTPUT_DIR, patient, 'Pre.nii.gz')
                    else:
                        Guessed_Name = mycopy(fullname, OUTPUT_DIR, patient, 'Pre.nii')
                if ADC:
                    if '.GZ' in fullname.upper():
                        Guessed_Name = mycopy(fullname, OUTPUT_DIR, patient, 'ADC.nii.gz')
                    else:
                        Guessed_Name = mycopy(fullname, OUTPUT_DIR, patient, 'ADC.nii')
                logfile.write(f'{fullname}, {Guessed_Name}\n')
                print(f'{fullname}, {Guessed_Name}\n')

logfile.close()
print("Done")