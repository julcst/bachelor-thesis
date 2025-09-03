import json
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
#plt.rcParams['legend.loc'] = 'upper right'

SMALL_SIZE = 6
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

def create_loss_history_plot(prefix: str, tests: list[(str, str)], size = (8, 1)):
    fig, ax = plt.subplots(figsize=size)
    for label, path in tests:
        with open(f"{prefix}{path}.hdr.json", "r") as f:
            data = json.load(f)
            iters = np.array(np.arange(data["total_samples"]))
            losses = np.array(data["loss_history"])
            ax.plot(iters, losses, label=label)
    ax.set_xlim(xmin=0)
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Relative L2 Loss")
    ax.legend()
    return fig, ax

fig, ax = create_loss_history_plot("tests/quality_comparison/", [
    ("NRC+PT", "nrc+pt_1spp"),
    ("NRC+PT+SL", "nrc+pt+sl_1spp"),
    ("NRC+BT", "nrc+bt_1spp"),
    ("NRC+LT", "nrc+lt_1spp"),
    ("NRC+SPPC", "nrc+sppc_1spp")
])
ax.set_ylim(ymin=0, ymax=5)
fig.savefig("loss_history.pgf", bbox_inches='tight')
plt.show()