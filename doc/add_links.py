 # -*- coding: utf-8 -*-

import os
import glob
import argparse

def make_argument_parser():
    '''Returns argument parser for this script.
    '''
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='''
This script adds links to each markdown file in the blog
========================================================

Each markdown file in stubs/ is converted and written to output/
                                     ''')

    fg = parser.add_argument_group('Flag parameters')
        
    fg.add_argument('--clean', action='store_true',
                    dest='clean_generated_files', 
                    default=False, 
                    help='If True, the generated Markdown files are removed. If False, they are generated.')

    return parser

def make_content_file_from_stub(stub_filename):

    md_filename = stub_filename.replace('stubs/', 'content/').replace('.md', '_GENERATED_by_add_links.md')
    link_filename = 'external_links.md'
    
    print('Reading stub file: {}'.format(stub_filename))
    with open(stub_filename, 'r') as f:
        stub_lines = f.readlines()

    print('Reading link file: {}'.format(link_filename))
    with open(link_filename, 'r') as f:
        link_lines = f.readlines()
        
    print('Adding links and making content file: {}'.format(md_filename))
    with open(md_filename, 'w') as f:
        for line in stub_lines + ['\n', '\n'] + link_lines:
            f.write(line)


def process_arguments(args):

    markdown_files = glob.glob('stubs/*.md') + glob.glob('stubs/pages/*.md')
    generated_files = glob.glob('content/*_GENERATED_by_add_links.md') \
                      + glob.glob('content/pages/*_GENERATED_by_add_links.md')
    
    if args.clean_generated_files:
        for gfn in generated_files:
            print('Removing generated file: {}'.format(gfn))
            os.remove(gfn)
    else:    
        for stub in markdown_files:
            make_content_file_from_stub(stub)
    
                    
if __name__ == '__main__':
    p = make_argument_parser()
    args = p.parse_args()
    process_arguments(args)
