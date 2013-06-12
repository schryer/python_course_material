'''
This module provides useful tools to use in other Python programs.
'''

__all__ = ['show', 'make_sequence_table']

from io import BytesIO

import matplotlib.pyplot as plt
from IPython.display import display, SVG

from ipytables import Table, TableCell

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

def make_sequence_table(seq0, seq1, display_length=30, colour_differences=True):
    '''
    Makes an HTML table representation to compare two sequences of strings.

    Parameters:
    -----------

    seq0 : str or equiv

    seq1 : str or equiv (same length or longer than seq0)

    display_length: int (default 30)
                    Length of each row in the table.

    colour_differences: bool (default True)
                        When True, each letter in the second sequence that does not match
                        with the letter found at the same index in the first sequence are
                        coloured red. 
    '''
    seq_table = Table()
    first_index = 0
    table_width = display_length
    cut_range = range(table_width, len(seq0)+table_width, table_width)
    for second_index in cut_range:
        first_segment = seq0[first_index:second_index]
        second_segment = seq1[first_index:second_index]

        first_row = []
        blank_row = []
        second_row = []
        for letter_index, S in enumerate(second_segment):
            F = first_segment[letter_index]
            tc = 'black'
            if F != S and F != '-':
                tc = 'red'

            first_row.append(TableCell(F, bg_colour='LightGrey'))
            second_row.append(TableCell(S, bg_colour='LightYellow', text_colour=tc))
            blank_row.append(TableCell(''))
        seq_table.append_row(first_row)
        seq_table.append_row(second_row)
        seq_table.append_row(blank_row)

        first_index = second_index
    return seq_table      	