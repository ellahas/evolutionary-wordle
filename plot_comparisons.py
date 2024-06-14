import numpy as np
import matplotlib.pyplot as plt

folder = "./5-mutation_fitness/"
times = np.load(folder+"times.npy")
generations = np.load(folder+"generations.npy")
individuals = np.load(folder+"individuals.npy")

colours = ["g", "y", "gray"]

ax1 = plt.subplot(2, 11, (1, 10))
bplot = ax1.boxplot(times[:-1,:].T, labels=["G", "", "", "G + Y", "", "", "G + Y\nweighted", "", "", "without\nreplacement"], medianprops={"color": "k"}, patch_artist=True)
ax1.set_ylabel("time (s)")
ax1.set_title("Time and Individuals until solution")

for i, patch in enumerate(bplot['boxes']):
    if i >= 9:
        patch.set_facecolor("w")
    else:
        patch.set_facecolor(colours[i % 3])

ax1.legend([bplot['boxes'][0], bplot['boxes'][1], bplot['boxes'][2], bplot['boxes'][9]], ["default mutation", "within word mutation", "within word, exclude self-swap", "brute-force"])

ax2 = plt.subplot(2, 11, 11)
bplot = ax2.boxplot(times[-1, :], labels=["with\nreplacement"], medianprops={"color": "k"}, patch_artist=True)
bplot['boxes'][0].set_facecolor("w")
ax2.yaxis.tick_right()

ax4 = plt.subplot(2, 1, 2)
ax4.set_ylabel("individuals")
bplot = ax4.boxplot(individuals.T, labels=["G", "", "", "G + Y", "", "", "G + Y\nweighted", "", "", "without\nreplacement", "with\nreplacement"], medianprops={"color": "k"}, patch_artist=True)

for i, patch in enumerate(bplot['boxes']):
    if i >= 9:
        patch.set_facecolor("w")
    else:
        patch.set_facecolor(colours[i % 3])

plt.tight_layout()
plt.show()
