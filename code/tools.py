'''
This module provides useful tools to use in other Python programs.
'''

__all__ = ['show']

from io import BytesIO

import matplotlib.pyplot as plt
from IPython.display import display, SVG

def fig_to_svg(fig, filename=None):
    output = BytesIO()
    
    fig.savefig(output, format='svg', bbox_inches='tight')

    if filename:
        filetype = filename.split('.')[-1]
        print('Saving: {0}  (filetype: {1})'.format(filename, filetype))
        fig.savefig(filename, format=filetype, bbox_inches='tight')        
    
    plt.close(fig)
    return output.getvalue()

def show(fig, **kwds):
    '''
    Displays an svg figure in IPython with the option of saving to disk.

    Parameters
    ----------
    fig : matplotlib figure object.

    filename : str (optional)
    
               If provided, the plot is saved to this filename.
               The file type is determined from the filename extension.
    '''
    display(SVG(fig_to_svg(fig, **kwds)))
