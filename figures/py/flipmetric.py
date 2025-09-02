import cv2
import flip_evaluator as flip
import numpy as np
import os

def load_hdr(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)  # float32 BGR
    if img is None:
        raise FileNotFoundError(f"Could not read HDR image: {path}")
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # HxWxC RGB float32

def to_srgb(img):
    return np.where(
        img <= 0.0031308,
        img * 12.92,
        1.055 * np.power(img, 1/2.4) - 0.055
    )

# Convert float images to 8-bit [0,255] for PNG output
def to_uint8(img):
    img_clipped = np.clip(img, 0, 1)  # HDR might exceed 1
    return (img_clipped * 255).astype(np.uint8)

def write_png(path, img, srgb=True): # img is float32 RGB
    if srgb:
        img = to_srgb(img)
    img = cv2.cvtColor(to_uint8(img), cv2.COLOR_RGB2BGR)  # Convert back to BGR
    cv2.imwrite(path, img)

def save_flip_png(ref_img, test_path: str):
    # Load HDRs as numpy arrays (HxWxC)
    test_img = load_hdr(f"{test_path}.hdr")

    # Run FLIP on numpy arrays
    flip_map, mean_error, params = flip.evaluate(
        reference=ref_img,
        test=test_img,
        dynamicRangeString="HDR",
    )

    # Save PNGs
    write_png(f"{test_path}.png", test_img)
    write_png(f"{test_path}_flip.png", flip_map, srgb=False)
    return mean_error

def save_flip_pngs(prefix: str, ref: str, tests: list[str], latex_prefix="figures/py/"):
    ref_img = load_hdr(f"{prefix}{ref}.hdr")
    write_png(f"{prefix}{ref}.png", ref_img)
    row1 = f"\\includegraphics[width=\\linewidth]{{{latex_prefix}{prefix}{ref}.png}}\n"
    row2 = ""
    means = "\\FLIP:"
    for test in tests:
        mean_error = save_flip_png(ref_img, f"{prefix}{test}")
        row1 += f"& \\includegraphics[width=\\linewidth]{{{latex_prefix}{prefix}{test}.png}}\n"
        row2 += f"& \\includegraphics[width=\\linewidth]{{{latex_prefix}{prefix}{test}_flip.png}}\n"
        means += f"& {mean_error:.3f}"
    with open(f"{prefix}table.tex", "w") as f:
        f.write(f"{row1}\\\\\n{row2}\\\\\n{means}\\\\\n")

save_flip_pngs("tests/path_termination/", "ref_1min", [
    "ref_1spp",
    "1stvert_1spp",
    "1stdiff_1spp",
    "sah_1spp",
    "bth_1spp",
    "bthk9_1spp",
])