import json
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'

def plot_breakdown(label_file_pairs, size=(6, 4), bar_width=0.1):
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

    fig, ax = plt.subplots(figsize=size)
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
                color = cmap(0.3 + 0.5*(i/n)) if hasattr(cmap, "__call__") else cmap
                bar = ax.bar(idx, val, color=color, bottom=bottom, width=bar_width,
                             label=k)
                ax.bar_label(bar, labels=[f"{val:.2f} ms"], label_type='center',
                             fontsize="xx-small", padding=2 if val < 0.15 else 0)
                bottom += val

        # Total label above bar
        ax.text(idx, bottom + 0.4, f"{breakdown['total']:.2f} ms",
                ha='center', va='bottom', fontsize="small", fontweight='bold')

    # Deduplicate legend entries and sort them according to ordered_keys
    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles)) # Deduplicate
    newh, newl = [], []
    for label in ordered_keys:
        if label in unique:
            newl.append(label)
            newh.append(unique[label])
    ax.legend(newh, newl, fontsize="xx-small")

    # Use provided labels for x-axis
    ax.set_ylabel("Time (ms)")
    #ax.set_title("Performance Breakdown")
    ax.set_xticks(x_positions)
    ax.set_xticklabels([lbl for lbl, _ in label_file_pairs])
    plt.tight_layout()
    #plt.show()

    return fig, ax

fig, ax = plot_breakdown([
    ("PT", "tests/caustic_small_reference_30min.hdr.json"),
    ("PM", "tests/caustic_small_photon_1spp.hdr.json")
])
fig.savefig("breakdown.pgf", bbox_inches='tight')