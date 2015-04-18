def adjust_spines(ax,spines=['bottom','left']):
	for loc, spine in ax.spines.iteritems():
		if loc in spines:
			spine.set_position(('outward',10))
			#spine.set_smart_bounds(True) #Doesn't work for log log plots
			spine.set_linewidth(1)
		else:
			spine.set_color('none') 
	if 'left' in spines:
		ax.yaxis.set_ticks_position('left')
	else:
		ax.yaxis.set_ticks([])

	if 'bottom' in spines:
		ax.xaxis.set_ticks_position('bottom')
	else:
		ax.xaxis.set_ticks([])

format = lambda text: r'\Large \textbf{%s}'%text