
from matplotlib import pyplot as plt
import numpy as np
import glob

# mine 
import patch_loader as pl


# params
TARGET_ASPECT = 1.6 # width to length aspect ratio
FIGURE_WIDTH = 12
FIGSIZE = np.array([FIGURE_WIDTH, FIGURE_WIDTH/TARGET_ASPECT])

##

def get_grid_size(c, a):
    '''
    Given an integer number of panels 
    and target aspect ratio, returns 
    an integer (width, height) which 
    best matches.
    Inputs: c, integer (total desired panels)
            a, float (target aspect ratio width/height)
    Outputs: m,n integers
    '''
    m = np.sqrt(c/a)
    m = int(m) + (m!=int(m))
    n = int(np.sqrt(c*a))
    if m*n<c:
        print('uh oh')
        n += 1
    return m,n

def clean_ax(someax):
    '''
    Removes spines and ticks from pyplot axis
    '''
    for s in someax.spines.values():
        s.set_visible(False)
    someax.set_xticks([])
    someax.set_yticks([])
    return # nothing to return

def plot_patch(patch, someax):
    '''
    Uses given json file and plots it in the given 
    pyplot axis given the student's parameters
    '''
    someax.pcolor(patch['reals'], patch['imags'], patch['array'], cmap=getattr(plt.cm, patch['colormap_name']), shading='auto')
    # TODO: set text color relative to local color.
    someax.text(0.02, 0.02, patch['attribution'], c='w', fontsize=10, transform=someax.transAxes)
    return

# Get a list of all file names 
# in the folder "data" whose filename 
# ends in ".json"
filenames = glob.glob("data/*.json")
submissions = []

# Create a list of dictionaries of objects.
for f in filenames:
    try:
        submissions.append( pl.import_patch(f) )
    except:
        # errors in loading
        print(f)
#

#count = len(submissions)
count = 8 # just to test

m,n = get_grid_size(count, TARGET_ASPECT)

names = [s['attribution'] for s in submissions]
order = np.argsort(names)

#
fig,ax = plt.subplots(m,n,
                      figsize=FIGSIZE, 
                      gridspec_kw={'wspace': 0, 'hspace': 0}
                      )

k = 0
for o in order[:count]:
    i = int(k//n)
    j = k%n
    print(k,i,j)
    print(submissions[o]['attribution'])
    clean_ax(ax[i,j])
    plot_patch(submissions[o], ax[i,j])
    
    k += 1

fig.tight_layout()
fig.savefig('test.pdf')
#fig.show()
