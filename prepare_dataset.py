import os
import shutil
import random

# Path to the extracted dataset (where all "Case XXX" folders are)
RAW_DIR = "raw_dicom_cases"
TARGET_DIR = "dicom"
TRAIN_DIR = os.path.join(TARGET_DIR, "train")
TEST_DIR = os.path.join(TARGET_DIR, "test")


def prepare_dataset():
    os.makedirs(TRAIN_DIR, exist_ok=True)
    os.makedirs(TEST_DIR, exist_ok=True)

    patient_folders = [
        f for f in os.listdir(RAW_DIR)
        if os.path.isdir(os.path.join(RAW_DIR, f))
    ]
    random.shuffle(patient_folders)

    split_idx = int(0.8 * len(patient_folders))
    train_folders = patient_folders[:split_idx]
    test_folders = patient_folders[split_idx:]

    def copy_dicom_folders(folders, dest_dir, set_name):
        count = 0
        for idx, folder in enumerate(folders):
            src = os.path.join(RAW_DIR, folder, "DICOM")
            dest = os.path.join(dest_dir, str(idx))

            if not os.path.exists(src):
                print(f"⚠️ Skipping '{folder}' in {set_name} set: No DICOM folder found.")
                continue

            shutil.copytree(src, dest)
            count += 1
        return count

    train_count = copy_dicom_folders(train_folders, TRAIN_DIR, "train")
    test_count = copy_dicom_folders(test_folders, TEST_DIR, "test")

    print(f"✅ Done! {train_count} train cases, {test_count} test cases copied.")


if __name__ == "__main__":
    prepare_dataset()
