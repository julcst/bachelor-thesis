import json
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
#plt.rcParams['font.family'] = 'Futura'
#plt.rcParams['legend.framealpha'] = 0.4

def plot_breakdown(label_file_pairs, size=(6, 3), bar_width=0.5, headroom=1.1, legloc='outside left center'):
    """
    Plot stacked bar breakdowns for one or more JSON files.

    Parameters
    ----------
    label_file_pairs : list of (str, str)
        List of (label, json_file_path) pairs.
    title : str
        Title of the plot.

    Returns
    -------
    fig, ax : matplotlib Figure and Axes
    """

    ordered_keys = [
        "photonQueryGeneration",
        "photonQueryMapBuildTime",
        "photonGeneration",
        "photonPostprocessing",
        "forwardSampleGeneration",
        "backwardSampleGeneration",
        "balanceSampleGeneration",
        "selfLearningInference",
        "selfLearningPostprocessing",
        "training",
        "pathtracing",
        "inference",
        "visualization",
        "other"
    ]

    groups = {
        "Photon": ["photonQueryGeneration", "photonQueryMapBuildTime", "photonGeneration", "photonPostprocessing"],
        "Sample Generation": ["forwardSampleGeneration", "backwardSampleGeneration", "balanceSampleGeneration"],
        "Self Learning": ["selfLearningInference", "selfLearningPostprocessing"],
        "Pathtracing & Inference": ["training", "pathtracing", "inference"],
        "Visualization": ["visualization"]
    }

    group_cmaps = {
        "Photon": cm.Oranges,
        "Sample Generation": cm.Blues,
        "Self Learning": cm.Greens,
        "Pathtracing & Inference": cm.Greys,
        "Visualization": "pink",
        "Other": "orchid"
    }

    fig, ax = plt.subplots(figsize=size, layout='constrained')
    x_positions = np.arange(len(label_file_pairs))

    for idx, (label, file) in enumerate(label_file_pairs):
        with open(file) as f:
            data = json.load(f)

        breakdown = data["breakdown"]

        # Filter out tiny timings (<0.02 ms), except total
        breakdown = {k: v for k, v in breakdown.items() if v >= 0.02 or k == "total"}

        # Compute 'other'
        sum_known = sum(breakdown.get(k, 0) for k in ordered_keys)
        breakdown["other"] = breakdown["total"] - sum_known
        groups["Other"] = ["other"]

        bottom = 0
        for group, keys in groups.items():
            cmap = group_cmaps[group]
            n = len(keys)
            for i, k in enumerate(keys):
                if k not in breakdown:
                    continue
                val = breakdown[k]
                color = cmap(0.2 + 0.6*(i/n)) if hasattr(cmap, "__call__") else cmap
                bar = ax.bar(idx, val, color=color, bottom=bottom, width=bar_width,
                             label=k)
                ax.bar_label(bar, labels=[f"{val:.2f} ms"], label_type='center',
                             fontsize="xx-small", padding=2 if val < 0.15 else 0)
                bottom += val

        # Total label above bar
        #ax.text(idx, bottom + 0.5, f"{breakdown['total']:.2f} ms", ha='center', va='bottom', fontsize="small", fontweight='bold')
        ax.annotate(f"{breakdown['total']:.2f} ms", xy=(idx, bottom), xytext=(0, 1), textcoords='offset fontsize', ha='center', va='bottom', fontsize="small", fontweight='bold', annotation_clip=False)

    # Deduplicate legend entries and sort them according to ordered_keys
    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles)) # Deduplicate
    newh, newl = [], []
    for label in ordered_keys:
        if label in unique:
            newl.append(label)
            newh.append(unique[label])
    if legloc.startswith('outside'):
        fig.legend(newh, newl, fontsize="xx-small", loc=legloc)
    else:
        ax.legend(newh, newl, fontsize="xx-small", loc=legloc)

    # Use provided labels for x-axis
    ax.set_ylabel("Time (ms)")
    _, ymax = ax.get_ylim()
    ax.set_ylim(ymax=ymax*headroom)
    #ax.set_title("Performance Breakdown")
    ax.set_xticks(x_positions)
    ax.set_xticklabels([lbl for lbl, _ in label_file_pairs], fontsize="x-small")

    return fig, ax

fig, ax = plot_breakdown([
    ("PT", "tests/quality_comparison/pt_1spp_thinker.hdr.json"),
    ("NRC+PT", "tests/quality_comparison/nrc+pt_1spp_thinker.hdr.json"),
    ("NRC+PT+SL", "tests/quality_comparison/nrc+pt+sl_1spp_thinker.hdr.json"),
    ("NRC+BT", "tests/quality_comparison/nrc+bt_1spp_thinker.hdr.json"),
    ("NRC+LT", "tests/quality_comparison/nrc+lt_1spp_thinker.hdr.json"),
    ("NRC+SPPC", "tests/quality_comparison/nrc+sppc_1spp_thinker.hdr.json"),
    ("PM", "tests/quality_comparison/sppm_1spp_thinker.hdr.json")
])
fig.savefig("breakdown.pgf", bbox_inches='tight')
#fig.savefig("breakdown.pdf", bbox_inches='tight')

fig, ax = plot_breakdown([
    ("NRC+PT", "tests/jit/nrc+pt_1spp.hdr.json"),
    ("+Fused", "tests/jit/nrc+pt+JIT_1spp.hdr.json"),
    ("+FusedVis", "tests/jit/nrc+pt+fullJIT_1spp.hdr.json"),
], size=(4, 2), headroom=1.3)
fig.savefig("jit.pgf", bbox_inches='tight')
#fig.savefig("jit.pdf", bbox_inches='tight')

import glob, re, os

def get_perf_files(folder, prefix):
    """Return sorted list of (label, path) for a given prefix."""
    pattern = re.compile(rf"{re.escape(prefix)}_(\d+)px\.hdr\.json")
    files = sorted(
        [(f"${m.group(1)}^2$px", path) 
         for path in glob.glob(os.path.join(folder, f"{prefix}_*px.hdr.json"))
         if (m := pattern.search(os.path.basename(path)))],
        key=lambda x: int(x[0][1:-5])
    )
    return files

def overlay_totals(ax, files, label, style, color=None):
    """Overlay total times as a line plot on the given axes."""
    xs, ys = [], []
    for lbl, path in files:
        with open(path) as f:
            data = json.load(f)
        xs.append(lbl)
        ys.append(data["breakdown"]["total"])
    ax.plot(xs, ys, style, label=label, color=color)

pt = get_perf_files("tests/performance_resolution", "pt_1spp")
nrc_pt = get_perf_files("tests/performance_resolution", "nrc+pt_1spp")
nrc_sppc = get_perf_files("tests/performance_resolution", "nrc+sppc_1spp")
fig, ax = plot_breakdown(nrc_sppc)
overlay_totals(ax, pt, "PT", '.--', 'black')
overlay_totals(ax, nrc_pt, "NRC+PT", '.--', 'purple')
fig.savefig("perfres.pgf", bbox_inches='tight')
#fig.savefig("perfres.pdf", bbox_inches='tight')

plt.show()