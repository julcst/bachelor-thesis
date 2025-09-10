import cv2
import flip_evaluator as flip
import numpy as np
import json
import os.path

COMPRESSION = 0 # PNG compression level [0-9], 0=none, 9=max
SCALE = 0.5 # Downscale factor

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
    if SCALE != 1.0:
        img = cv2.resize(img, None, fx=SCALE, fy=SCALE)
    cv2.imwrite(path, img, [cv2.IMWRITE_PNG_COMPRESSION, COMPRESSION])

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

from dataclasses import dataclass

@dataclass
class TestResult:
    name: str
    duration: float
    samples: int
    flip: float
    mse: float
    bias2: float | None
    var: float | None

# Helpers
def bold_if_min(val, min_val, fmt, none_allowed=False):
    if val is None and none_allowed:
        return ""
    s = fmt(val)
    if min_val is not None and val == min_val:
        return f"\\textbf{{{s}}}"
    return s

def save_flip_pngs(prefix: str, ref: str, tests: list[str], suffix="", msuffix="", latex_prefix="figures/py/", table_name="table", enable_flip_row=True):
    print(f"Creating {prefix}{table_name}...")
    ref_img = load_hdr(f"{prefix}{ref}.hdr")
    write_png(f"{prefix}{ref}.png", ref_img)

    # Collect results
    results: list[TestResult] = []
    for test in tests:
        print(f"{ref} vs {test}")
        flip_mean, mse = save_flip_png(ref_img, f"{prefix}{test}{suffix}")

        with open(f"{prefix}{test}{suffix}.hdr.json", "r") as f:
            data = json.load(f)

        try:
            mean = load_hdr(f"{prefix}{test}{msuffix}_mean.hdr")
            var = load_hdr(f"{prefix}{test}{msuffix}_var.hdr")
            b, v = calc_biasvar(ref_img, mean, var)
            b2 = b * b
        except FileNotFoundError:
            b2, v = None, None

        results.append(TestResult(
            name=test,
            duration=data["duration"],
            samples=data["samples"],
            flip=flip_mean,
            mse=mse,
            bias2=b2,
            var=v,
        ))

    # Find minima
    min_duration = min(r.duration for r in results)
    min_flip     = min(r.flip for r in results)
    min_mse      = min(r.mse for r in results)
    min_bias     = min((r.bias2 for r in results if r.bias2 is not None), default=None)
    min_var      = min((r.var   for r in results if r.var   is not None), default=None)

    # Build LaTeX rows
    perf_row = get_perf(f"{prefix}{ref}")
    img_row  = f"\\includegraphics[width=\\linewidth]{{{latex_prefix}{prefix}{ref}.png}}\n"
    flip_row, error_row, bias_var_row = "", "", ""

    for r in results:
        # perf
        dur_str = bold_if_min(r.duration, min_duration, format_seconds)
        perf_row += f" & {r.samples}spp ({dur_str})\n"

        # error row
        flip_str = bold_if_min(r.flip, min_flip, lambda x: f"\\num{{{x:.3f}}}")
        mse_str  = bold_if_min(r.mse,  min_mse,  lambda x: f"\\num{{{x:.3f}}}")
        error_row += f" & {flip_str}/{mse_str}\n"

        # bias/var
        if r.bias2 is not None and r.var is not None:
            bias_str = bold_if_min(r.bias2, min_bias, lambda x: f"\\num{{{x:.2e}}}")
            var_str  = bold_if_min(r.var,   min_var,  lambda x: f"\\num{{{x:.2e}}}")
            bias_var_row += f" & {bias_str}/{var_str}\n"
        else:
            bias_var_row += " &\n"

        # images
        img_row  += f"& \\includegraphics[width=\\linewidth]{{{latex_prefix}{prefix}{r.name}{suffix}.png}}\n"
        flip_row += f"& \\includegraphics[width=\\linewidth]{{{latex_prefix}{prefix}{r.name}{suffix}_flip.png}}\n"

    with open(f"{prefix}{table_name}.tex", "w") as f:
        f.write(f"&{perf_row}\\\\\n"
                f"\\rotatebox{{90}}{{\\textsc{{{table_name}}}}}\\hspace{{-1.5em}}\n"
                f"&{img_row}\\\\\n"
                + (f"&{flip_row}\\\\\n" if enable_flip_row else "") +
                f"&\\FLIP/MSE:{error_row}\\\\\n"
                f"&$\\mathrm{{Bias}}^2/\\mathrm{{Variance}}${bias_var_row}\\\\\n")

convert_to_png("tests/path_termination/rawcache_1spp_thinker")

save_flip_pngs("tests/path_termination/", "ref_1min_thinker", [
    "ref",
    "sah",
    "bth",
    "bthk9",
    "1stdiff",
    "1stvert",
], suffix="_1spp_thinker", msuffix="_thinker", table_name="Thinker")

save_flip_pngs("tests/path_termination/", "ref_1min_thinker", [
    "ref",
    "sah+nee",
    "bth+nee",
    "bthk9+nee",
    "1stdiff+nee",
    "1stvert+nee",
], suffix="_1spp_thinker", msuffix="_thinker", table_name="Thinker+NEE")

save_flip_pngs("tests/encodings/", "../quality_comparison/refpt_3min_thinker", [
    "nrc+ptTWE",
    "nrc+ptMHE",
], suffix="_1spp", msuffix="", table_name="Thinker")

save_flip_pngs("tests/batch_size/", "../quality_comparison/refpt_3min_thinker", [
    "1+nrc+pt+14",
    "5+nrc+pt+14",
    "25+nrc+pt+14",
    "100+nrc+pt+14",
    "500+nrc+pt+14",
    "2500+nrc+pt+14",
], suffix="_1spp", msuffix="", table_name="14", enable_flip_row=False)

save_flip_pngs("tests/batch_size/", "../quality_comparison/refpt_3min_thinker", [
    "1+nrc+pt+14@4",
    "5+nrc+pt+14@4",
    "25+nrc+pt+14@4",
    "100+nrc+pt+14@4",
    "500+nrc+pt+14@4",
    "2500+nrc+pt+14@4",
], suffix="_1spp", msuffix="", table_name="14@4", enable_flip_row=False)

save_flip_pngs("tests/batch_size/", "../quality_comparison/refpt_3min_thinker", [
    "1+nrc+pt+16",
    "5+nrc+pt+16",
    "25+nrc+pt+16",
    "100+nrc+pt+16",
    "500+nrc+pt+16",
    "2500+nrc+pt+16",
], suffix="_1spp", msuffix="", table_name="16", enable_flip_row=False)

save_flip_pngs("tests/batch_size/", "../quality_comparison/refpt_3min_thinker", [
    "1+nrc+pt+16@4",
    "5+nrc+pt+16@4",
    "25+nrc+pt+16@4",
    "100+nrc+pt+16@4",
    "500+nrc+pt+16@4",
    "2500+nrc+pt+16@4",
], suffix="_1spp", msuffix="", table_name="16@4", enable_flip_row=False)

save_flip_pngs("tests/quality_comparison/", "refpt_3min_diffuse", [
    "pt",
    "nrc+pt",
    "nrc+pt+sl",
    "nrc+bt",
    "nrc+lt",
    "nrc+sppc",
    "sppm"
], suffix="_1spp_diffuse", msuffix="_diffuse", table_name="Diffuse")

save_flip_pngs("tests/quality_comparison/", "refpt_3min_thinker", [
    "pt",
    "nrc+pt",
    "nrc+pt+sl",
    "nrc+bt",
    "nrc+lt",
    "nrc+sppc",
    "sppm"
], suffix="_1spp_thinker", msuffix="_thinker", table_name="Thinker")

save_flip_pngs("tests/quality_comparison/", "refpt_3min_chess", [
    "pt",
    "nrc+pt",
    "nrc+pt+sl",
    "nrc+bt",
    "nrc+lt",
    "nrc+sppc",
    "sppm"
], suffix="_1spp_chess", msuffix="_chess", table_name="Chess")

save_flip_pngs("tests/quality_comparison/", "refpt_3min_ajar_caustic", [
    "pt",
    "nrc+pt",
    "nrc+pt+sl",
    "nrc+bt",
    "nrc+lt",
    "nrc+sppc",
    "sppm"
], suffix="_1spp_ajar_caustic", msuffix="_ajar_caustic", table_name="Ajar")

save_flip_pngs("tests/quality_comparison/", "refsppm_2min", [
    "pt",
    "nrc+pt",
    "nrc+pt+sl",
    "nrc+bt",
    "nrc+lt",
    "nrc+sppc",
    "sppm"
], suffix="_1spp_caustics_small", msuffix="_caustics_small", table_name="Caustics")

save_flip_pngs("tests/quality_comparison/", "refpt_3min_diffuse", [
    "nrc+lt",
    "nrc+lt+bal",
    "nrc+lt+balcam",
    "nrc+naive",
    "nrc+naive+bal",
    "nrc+naive+balcam",
], suffix="_1spp_diffuse", msuffix="_diffuse", table_name="DiffuseBal")

save_flip_pngs("tests/quality_comparison/", "refpt_3min_thinker", [
    "nrc+lt",
    "nrc+lt+bal",
    "nrc+lt+balcam",
    "nrc+naive",
    "nrc+naive+bal",
    "nrc+naive+balcam",
], suffix="_1spp_thinker", msuffix="_thinker", table_name="ThinkerBal")

save_flip_pngs("tests/quality_comparison/", "refsppm_2min", [
    "nrc+lt",
    "nrc+lt+bal",
    "nrc+lt+balcam",
    "nrc+naive",
    "nrc+naive+bal",
    "nrc+naive+balcam",
], suffix="_1spp_caustics_small", msuffix="_caustics_small", table_name="CausticsBal")

save_flip_pngs("tests/photon_optimization/", "ref_2min", [
    "SER",
    "SER+Reject70",
    "SER+Reject70+RejectN"
], suffix="_1spp", table_name="Caustics")