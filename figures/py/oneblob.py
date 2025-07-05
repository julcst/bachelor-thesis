import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'

def quartic_cdf(x, inv_radius):
    u = x * inv_radius
    u2 = u * u
    u4 = u2 * u2
    cdf = (15.0/16.0) * u * (1 - (2.0/3.0) * u2 + (1.0/5.0) * u4) + 0.5
    return np.clip(cdf, 0.0, 1.0)

def cdf_no_wrap(x, inv_radius, edge=0):
    return quartic_cdf(edge - x, inv_radius)

def cdf_wrap(x, inv_radius, edge=0):
    return (
        quartic_cdf(edge - x, inv_radius) +
        quartic_cdf(edge - x - 1.0, inv_radius) +
        quartic_cdf(edge - x + 1.0, inv_radius)
    )

def cdf_reflected(x, inv_radius, edge=0):
    return (
        quartic_cdf(edge - x, inv_radius) +
        quartic_cdf(edge - (1.0 - x) - 1.0, inv_radius) +
        quartic_cdf(edge - (1.0 - x) + 1.0, inv_radius)
    )

def one_blob_field(x, num_bins_log2, cdf=cdf_no_wrap):
    n_bins = 1 << num_bins_log2
    inv_radius = n_bins

    field = np.zeros((n_bins, len(x)))

    left_cdf = cdf(x, inv_radius)

    for bi in range(n_bins):
        right_boundary = (bi + 1) * 2 ** -num_bins_log2
        right_cdf = cdf(x, inv_radius, right_boundary)
        field[bi, :] = right_cdf - left_cdf
        left_cdf = right_cdf
    
    return field

# Plot
x = np.linspace(0, 1, 100)

activations = one_blob_field(x, 2, cdf_wrap)
plt.figure(figsize=(5, 3))
for i, y in enumerate(activations):
    plt.plot(x, y, label=f'bin={i}')
plt.title("Wrapped Quartic Bin Integration")
plt.xlabel("Input Position x")
plt.xticks(np.linspace(0, 1, 5))
plt.ylabel("Bin Activation")
plt.legend()
plt.grid(True)
plt.savefig('oneblob_wrap.pgf', bbox_inches='tight')
plt.show()

activations = one_blob_field(x, 2, cdf_no_wrap)
plt.figure(figsize=(5, 3))
for i, y in enumerate(activations):
    plt.plot(x, y, label=f'bin={i}')
plt.title("Standard Quartic Bin Integration")
plt.xlabel("Input Position x")
plt.xticks(np.linspace(0, 1, 5))
plt.ylabel("Bin Activation")
plt.legend()
plt.grid(True)
plt.savefig('oneblob.pgf', bbox_inches='tight')
plt.show()

activations = one_blob_field(x, 2, cdf_reflected)
plt.figure(figsize=(8, 6))
for i, y in enumerate(activations):
    plt.plot(x, y, label=f'bin={i}')
plt.title("Reflected Quartic Bin Integration")
plt.xlabel("Input Position x")
plt.xticks(np.linspace(0, 1, 5))
plt.ylabel("Bin Activation")
plt.legend()
plt.grid(True)
plt.show()


# Compute the bin boundaries for bin 0
r = 0.125
l = -0.125

# Use same CDF as one_blob_field
cdf_bin0 = quartic_cdf(r-x, 4) - quartic_cdf(l-x, 4)

# Plot
plt.figure(figsize=(8, 6))
plt.plot(x, cdf_bin0, label='bin 0 activation (matched)')
plt.title("Wrapped Quartic Bin Integration (bin 0 matched)")
plt.xlabel("Input Position x")
plt.ylabel("Bin Activation")
plt.xticks([0.125, 0.375, 0.625, 0.875])
plt.legend()
plt.grid(True)
plt.show()