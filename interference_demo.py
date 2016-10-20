# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 11:09:27 2016

@author: michw
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation

makeimage = 0
makevideo = 1

f = 5000. # frequency (Hz)
c = 1500. # sound speed (m/s)
l = c/f # wavelength (m)
dx = l*.5 # element separation (m)
n = 2 # number of elements
k = 2*np.pi*f/c # wavenumber

# Set acoustic element coordinates
sy = np.zeros(n)
sx = np.arange(0,dx*n,dx)


# Construct background coordinates
res = 0.01
xmin = -3
xmax = np.max(sx)+3
ymin = -5
ymax = 0
xvals = np.arange(xmin,xmax,res)
yvals = np.arange(ymin,ymax,res)
gridx,gridy = np.meshgrid(xvals,yvals)

# Compute ranges from each element to each grid cell
ranges0 = []
for sdex in np.arange(n):
    ranges0.append(np.sqrt(((sx[sdex]-gridx)**2) + ((sy[sdex]-gridy)**2)))
ranges = np.array(ranges0)

# Compute summed complex amplitude at each grid cell 
i = np.sqrt(-1)

ampsum = sum(np.exp(1j*(k*ranges))/ranges)
ampsum = np.flipud(ampsum)

# Compute summed absolute amplitude at each grid cell

if makeimage == 1:
    plt.figure(1)
    plt.clf()
    plt.imshow(np.real(ampsum),
               extent = [min(xvals),max(xvals),
                         min(yvals),max(yvals)],
               vmin = -1, vmax = 1,cmap = 'RdBu')
    plt.scatter(sx,sy,s=5,c='k',edgecolor='black',linewidth=4,marker='s')
    plt.autoscale(tight = True)
    plt.xlabel('horizontal distance (m)')
    plt.ylabel('depth (m)')
    
    # Save figure
    filename = 'IMGintpattern_f' + str(np.round(f)) + '_n' + str(n) + '_dx' + str(dx) + '.png'
    plt.savefig(filename)




if makevideo == 1:
    # Create a movie by looping through angular steps
    FFMpegWriter = manimation.writers['ffmpeg']
    metadata = dict(title='Movie Test', artist='Matplotlib',
                    comment='Get your popcorn!')
    writer = FFMpegWriter(fps=15, metadata=metadata)
    
    tsteps = 10
    T = np.linspace(0,2*np.pi,tsteps)
    T = T[0:-1]
    reps = 10
    T = np.tile(T,reps)
    T = np.flipud(T)
    #
    fig = plt.figure(2)
    moviename = 'intpattern_f' + str(np.round(f)) + '_n' + str(n) + '_dx' + str(dx) + '.mp4'
    with writer.saving(fig, moviename, 300):
        for tdex in np.arange(len(T)):
            ampsum2 = np.real(ampsum*np.exp(1j*T[tdex]))
        
            plt.clf()
            plt.imshow(ampsum2,
                       extent = [min(xvals),max(xvals),
                                 min(yvals),max(yvals)],
                       vmin = -1, vmax = 1,cmap = 'RdBu')
            plt.scatter(sx,sy,s=120,c='w',edgecolor='black',linewidth=4)
            plt.autoscale(tight = True)
            plt.xlabel('horizontal distance (m)')
            plt.ylabel('depth (m)')
            
            writer.grab_frame()