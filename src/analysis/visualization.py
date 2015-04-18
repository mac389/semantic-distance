import graphics as artist
import matplotlib.pyplot as plt

from matplotlib import rcParams

rcParams['text.usetex'] = True

format_label = lambda text: r'\Large \textbf{\textsc{%s}}'%text

def heatmap(array):
	fig  = plt.figure()
	ax = fig.add_subplot(111)

	cax = ax.imshow(array,interpolation='nearest',aspect='auto',cmap = plt.cm.binary_r)
	artist.adjust_spines(ax)

	ax.set_ylabel(format_label('Abstract'))
	ax.set_xlabel(format_label('Abstract'))
	ax.set_title(format_label('Comparison of meaning of %d abstracts'%(array.size)))

	cbar = plt.colorbar(cax)
	cbar.set_label(format_label('Semantic Similarity'))
	plt.tight_layout()

	plt.show()