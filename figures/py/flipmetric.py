import cv2
import flip_evaluator as flip
import numpy as np
import json
import os.path

def load_hdr(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)  # float32 BGR
    if img is None:
        raise FileNotFoundError(f"Could not load image: {path}")
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
    flip_map, flip_mean, params = flip.evaluate(
        reference=ref_img,
        test=test_img,
        dynamicRangeString="HDR",
    )

    # Save PNGs
    write_png(f"{test_path}.png", test_img)
    write_png(f"{test_path}_flip.png", flip_map, srgb=False)
    return flip_mean, mse

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

def convert_to_png(path: str):
    img = load_hdr(f"{path}.hdr")
    write_png(f"{path}.png", img)

def calc_biasvar(ref_img, mean_img, var_img):
    bias = np.mean(mean_img - ref_img)
    variance = np.mean(var_img)
    return bias, variance

def save_flip_pngs(prefix: str, ref: str, tests: list[str], suffix="", msuffix="", latex_prefix="figures/py/", table_name="table"):
    print(f"Creating {prefix}{table_name}...")
    ref_img = load_hdr(f"{prefix}{ref}.hdr")
    write_png(f"{prefix}{ref}.png", ref_img)
    perf_row = get_perf(f"{prefix}{ref}")
    img_row = f"\\includegraphics[width=\\linewidth]{{{latex_prefix}{prefix}{ref}.png}}\n"
    flip_row = ""
    error_row = ""
    bias_var_row = ""
    for test in tests:
        print(f"{ref} vs {test}")
        flip_mean, mse = save_flip_png(ref_img, f"{prefix}{test}{suffix}")
        img_row += f"& \\includegraphics[width=\\linewidth]{{{latex_prefix}{prefix}{test}{suffix}.png}}\n"
        flip_row += f"& \\includegraphics[width=\\linewidth]{{{latex_prefix}{prefix}{test}{suffix}_flip.png}}\n"
        error_row += f" & ${flip_mean:.3f}/{mse:.3f}$"
        perf_row += f" & {get_perf(f"{prefix}{test}{suffix}")}"
        try:
            mean = load_hdr(f"{prefix}{test}{msuffix}_mean.hdr")
            var = load_hdr(f"{prefix}{test}{msuffix}_var.hdr")
            b, v = calc_biasvar(ref_img, mean, var)
            b2 = b * b
            bias_var_row += f" & ${b2:.2e}/{v:.2e}$"
        except FileNotFoundError:
            bias_var_row += " & "

    with open(f"{prefix}{table_name}.tex", "w") as f:
        f.write(f"{perf_row}\\\\\n{img_row}\\\\\n{flip_row}\\\\\n\\FLIP/MSE:{error_row}\\\\\n$\\mathrm{{Bias}}^2/\\mathrm{{Variance}}${bias_var_row}\\\\\n")

# TODO: Variance + Bias decomp

save_flip_pngs("tests/path_termination/", "ref_1min_thinker", [
    "ref",
    "1stvert",
    "1stdiff",
    "sah",
    "bth",
    "bthk9",
], suffix="_1spp_thinker", msuffix="_thinker")

save_flip_pngs("tests/quality_comparison/", "pt_1min", [
    "pt",
    "nrc+pt",
    "nrc+pt+sl",
    "nrc+bt",
    "nrc+lt",
    "nrc+sppc",
    "sppm"
], suffix="_1spp")