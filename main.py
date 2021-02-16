import nibabel as nib
import os
import PIL
import shutil


INPUT_DIR = "/research/proejcts/BrainAbscess/MR_Notion_february/"
OUTPUT_DIR = INPUT_DIR.replace("MR_Notion_february", "Sorted")

logfile = open(os.path.join(OUTPUT_DIR, 'log.txt'))

Patient_List = sorted(os.listdir(INPUT_DIR))

logfile.write('Original_Filename, Guessed_Name\n')

def mycopy(srcfile, tgdir, patient, type):
    # copy scrfile to tgdir/tgname
    # and write a PNG of central slice to that tgdir/PNG
    outfname = os.path.join(os.path.join(tgdir, patient), type)
    cmd = f'cp {srcfile} {outfname}'
    shutil(cmd)
    

for patient in Patient_List:
    Pre=None
    T2=None
    Post=None
    FLAIR=None
    ADC=None
    for series_dir in sorted(os.listdir(os.path.join(INPUT_DIR, patient))):
        fullname = os.path.join(os.path.join(INPUT_DIR, patient), series_dir).upper()
        if os.path.isdir(fullname):
            if 'FLAIR' in fullname and not 'T1' in fullname:
                FLAIR = True
            if 'T2' in fullname and not FLAIR:
                T2 = True
            if 'POST' in fullname or 'GD' in fullname or 'GAD' in fullname or 'WITH' in fullname:
                Post = True
            if 'PRE' in fullname or 'T1' in fullname:
                if not Post:
                    Pre = True
            if 'ADC' in fullname or 'APPARENT DIFF' in fullname:
                ADC=True
            if FLAIR:
                mycopy(fullname, OUTPUT_DIR, patient, 'FLAIR.nii')

