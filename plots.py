#!/usr/bin/env python
# module PLOTS
import matplotlib.pyplot as plt

def plot_picture(img_rgb,title='',colorbar=False, axis=False, filename=''):
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    #fig = plt.figure(frameon=False)
    fig = plt.figure()
    ax = plt.gca()
    im = ax.imshow(img_rgb)
    #ax.set_title(title)
    height, width = img_rgb.shape[:2]
    factor = 50
    fig.set_size_inches(width/factor, height/factor)

    if colorbar!='out':
        if colorbar=='in':
            #cax = fig.add_axes([0.05,0.5,0.02,0.45])
            cax = fig.add_axes([0.15,0.5,0.02,0.3])
            cb = plt.colorbar(im, cax=cax)
            cbytick_obj = plt.getp(cb.ax.axes, 'yticklabels')
            plt.setp(cbytick_obj,color='w',weight='bold',size='x-large')
            fig.add_axes(cax)
    else:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cb = plt.colorbar(im, cax=cax)
        fig.add_axes(cax)
    if not axis:
        ax.axis('off')
    if filename != '':
        plt.savefig(filename)
    plt.show()
