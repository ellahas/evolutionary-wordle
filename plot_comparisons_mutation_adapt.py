import numpy as np
import matplotlib.pyplot as plt

folder = "./5-mutation_adaptation/"
times = np.load(folder+"times.npy")
generations = np.load(folder+"generations.npy")
individuals = np.load(folder+"individuals.npy")

ax1 = plt.subplot(2, 6, (1, 5))
bplot = ax1.boxplot(times[:-1,:].T, labels=["constant", "deterministic", "amount correct", "Wang & Tang", "without\nreplacement"], medianprops={"color": "k"}, patch_artist=True)
ax1.set_ylabel("time (s)")
ax1.set_title("Time and Individuals until solution")

for i, patch in enumerate(bplot['boxes']):
    if i == 0:
        patch.set_facecolor("g")
    elif i < 4:
        patch.set_facecolor("y")
    else:
        patch.set_facecolor("w")

ax1.legend([bplot['boxes'][0], bplot["boxes"][1], bplot['boxes'][-1]], ["baseline", "adaptive mutation", "brute-force"])

ax2 = plt.subplot(2, 6, 6)
bplot = ax2.boxplot(times[-1, :], labels=["with\nreplacement"], medianprops={"color": "k"}, patch_artist=True)
bplot['boxes'][0].set_facecolor("w")
ax2.yaxis.tick_right()

ax4 = plt.subplot(2, 1, 2)
ax4.set_ylabel("individuals")
bplot = ax4.boxplot(individuals.T, labels=["constant", "deterministic", "amount correct", "Wang & Tang", "without\nreplacement", "with\nreplacement"], medianprops={"color": "k"}, patch_artist=True)

for i, patch in enumerate(bplot['boxes']):
    if i == 0:
        patch.set_facecolor("g")
    elif i < 4:
        patch.set_facecolor("y")
    else:
        patch.set_facecolor("w")

plt.tight_layout()
plt.show()
