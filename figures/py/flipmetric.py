import cv2
import flip_evaluator as flip
import numpy as np
import json

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
    cv2.imwrite(path, img, [cv2.IMWRITE_PNG_COMPRESSION, 9])

def save_flip_png(ref_img, test_path: str):
    # Load HDRs as numpy arrays (HxWxC)
    test_img = load_hdr(f"{test_path}.hdr")
    mse = np.mean((ref_img - test_img) ** 2)

    # Run FLIP on numpy arrays
    flip_map, mean_error, params = flip.evaluate(
        reference=ref_img,
        test=test_img,
        dynamicRangeString="HDR",
    )

    # Save PNGs
    write_png(f"{test_path}.png", test_img)
    write_png(f"{test_path}_flip.png", flip_map, srgb=False)
    return mean_error, mse

def format_seconds(seconds: float) -> str:
    if seconds < 1:
        return f"{seconds * 1000:.2f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 360:
        return f"{seconds / 60:.0f}m"
    return f"{seconds // 360:.0f}h"

def get_perf(path: str) -> str:
    with open(f"{path}.hdr.json", "r") as f:
        data = json.load(f)
        return f"{data['samples']}spp ({format_seconds(data['duration'])})\n"

def save_flip_pngs(prefix: str, ref: str, tests: list[str], latex_prefix="figures/py/", table_name="table"):
    print(f"Creating {prefix}{table_name}...")
    ref_img = load_hdr(f"{prefix}{ref}.hdr")
    write_png(f"{prefix}{ref}.png", ref_img)
    perf_row = get_perf(f"{prefix}{ref}")
    img_row = f"\\includegraphics[width=\\linewidth]{{{latex_prefix}{prefix}{ref}.png}}\n"
    flip_row = ""
    flip_means = ""
    rmse_row = ""
    for test in tests:
        print(f"{ref} vs {test}")
        mean_error, mse = save_flip_png(ref_img, f"{prefix}{test}")
        img_row += f"& \\includegraphics[width=\\linewidth]{{{latex_prefix}{prefix}{test}.png}}\n"
        flip_row += f"& \\includegraphics[width=\\linewidth]{{{latex_prefix}{prefix}{test}_flip.png}}\n"
        flip_means += f"& {mean_error:.3f}"
        rmse_row += f"& {np.sqrt(mse):.3f}"
        perf_row += f"& {get_perf(f"{prefix}{test}")}"
            
    with open(f"{prefix}{table_name}.tex", "w") as f:
        f.write(f"{perf_row}\\\\\n{img_row}\\\\\n{flip_row}\\\\\n\\FLIP:{flip_means}\\\\\nRMSE:{rmse_row}\\\\\n")

# TODO: Variance + Bias decomp

save_flip_pngs("tests/path_termination/", "ref_1min", [
    "ref_1spp",
    "1stvert_1spp",
    "1stdiff_1spp",
    "sah_1spp",
    "bth_1spp",
    "bthk9_1spp",
])

save_flip_pngs("tests/quality_comparison/", "pt_1min", [
    "pt_1spp",
    "nrc+pt_1spp",
    "nrc+pt+sl_1spp",
    "nrc+bt_1spp",
    "nrc+lt_1spp",
    "nrc+sppc_1spp",
    "sppm_1spp"
])