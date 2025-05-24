import os
import pydicom
import numpy as np
from skimage import filters, morphology, measure
import matplotlib.pyplot as plt

def load_dicom_series(folder_path):
    """Load all .dcm files in a folder into a 3D NumPy array."""
    slices = []
    for fn in sorted(os.listdir(folder_path)):
        if fn.lower().endswith('.dcm'):
            ds = pydicom.dcmread(os.path.join(folder_path, fn))
            slices.append(ds)
    if not slices:
        raise FileNotFoundError(f"No DICOM files in {folder_path}")
    # Optional sort by SliceLocation
    try:
        slices.sort(key=lambda s: float(s.SliceLocation))
    except: pass
    volume = np.stack([s.pixel_array for s in slices], axis=0)
    return volume

def segment_volume(volume, method='otsu'):
    """Segment 3D volume via Otsu thresholding (or adaptive)."""

    # 🛡️ Add safety check for tiny or malformed volumes
    if volume.shape[0] < 2 or volume.shape[1] < 2 or volume.shape[2] < 2:
        raise ValueError("Volume too small for segmentation.")

    if method == 'otsu':
        thresh = filters.threshold_otsu(volume)
        mask = volume > thresh
    else:
        raise ValueError("Unsupported method")

    # Clean up
    mask = morphology.remove_small_objects(mask, min_size=64)
    mask = morphology.remove_small_holes(mask, area_threshold=64)
    return mask

def compute_mask_features(volume, mask, voxel_spacing=(1.0,1.0,1.0)):
    """
    Compute:
      - volume_cm3: total voxels * voxel volume (mm^3→cm^3)
      - mean_area_px: mean mask pixels per slice
      - surface_area_cm2: mesh surface area (mm^2→cm^2)
    """
    # 1) Volume
    voxel_vol_mm3 = np.prod(voxel_spacing)
    total_voxels  = mask.sum()
    volume_cm3    = total_voxels * voxel_vol_mm3 / 1000.0

    # 2) Mean area per slice
    mean_area_px = float(mask.sum(axis=(1,2)).mean())

    # 3) Surface area via marching cubes
    verts, faces, _, _ = measure.marching_cubes(
        mask.astype(float), level=0.5, spacing=voxel_spacing
    )
    surface_mm2  = measure.mesh_surface_area(verts, faces)
    surface_cm2  = surface_mm2 / 100.0

    return {
        'volume_cm3': round(volume_cm3,2),
        'mean_area_px': round(mean_area_px,1),
        'surface_area_cm2': round(surface_cm2,2)
    }

def plot_slice_mask(volume, mask, slice_index, figsize=(8, 4)):
    """
    Plot a single slice of the volume alongside its segmentation mask.
    """
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    axes[0].imshow(volume[slice_index], cmap='gray')
    axes[0].set_title(f"Slice {slice_index}")
    axes[0].axis('off')

    axes[1].imshow(volume[slice_index], cmap='gray')
    axes[1].imshow(mask[slice_index], cmap='jet', alpha=0.5)
    axes[1].set_title("Segmentation Mask")
    axes[1].axis('off')

    plt.tight_layout()
    return fig
