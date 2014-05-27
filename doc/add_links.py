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

def make_content_file_from_stub(stub_filename, link_lines):

    md_filename = stub_filename.replace('stubs/', 'content/').replace('.md', '_GENERATED_by_add_links.md')
    
    print('Reading stub file: {}'.format(stub_filename))
    with open(stub_filename, 'r') as f:
        stub_lines = f.readlines()
        
    print('Adding links and making content file: {}'.format(md_filename))
    with open(md_filename, 'w') as f:
        for line in stub_lines + ['\n', '\n'] + link_lines:
            f.write(line)

def make_content_file_from_ipynb(ipynb_filename, link_lines):
    
    temp_md_filename = ipynb_filename.replace('stubs/', '').replace('.ipynb', '.md')
    md_filename = ipynb_filename.replace('stubs/', 'content/').replace('.ipynb', '_GENERATED_by_add_links.md')
    
    article_elements = temp_md_filename.replace('.md', '').split('_')
    article_number = article_elements[0]
    article_title = ' '.join(article_elements[1:]).title()
    title = 'Lesson {}: {}.'.format(article_number, article_title)
    
    header_lines = ['Author: David Schryer',
                    'Category: article',
                    'Date: 2014-05-21 12:00',
                    'Slug: Python{}'.format(article_number),
                    'Summary: {}'.format(title),
                    'Tags: Python',
                    'Title: {}'.format(title),
                    'URL: python/{}'.format(article_number),
                    'save_as: python/{}/index.html'.format(article_number),
                ]
    
    cmd = 'ipython nbconvert --to markdown {}'.format(ipynb_filename)
    print('Executing: {}'.format(cmd))
    os.system(cmd)

    print('Reading markdown file: {}'.format(temp_md_filename))
    with open(temp_md_filename, 'r') as f:
        md_lines = f.readlines()
        
    print('Adding header info and links to make content file: {}'.format(md_filename))
    with open(md_filename, 'w') as f:
        for line in header_lines:
            f.write(line + '\n')
        for line in md_lines + ['\n', '\n'] + link_lines:
            f.write(line)

    cmd = 'rm {}'.format(temp_md_filename)
    print('Removing temporary Markdown file by executing: {}'.format(cmd))
    os.system(cmd)
    

def convert_files(args):

    link_filename = 'external_links.md'

    markdown_files = glob.glob('stubs/*.md') + glob.glob('stubs/pages/*.md')
    ipython_files = glob.glob('stubs/*.ipynb') 
    generated_files = glob.glob('content/*_GENERATED_by_add_links.md') \
                      + glob.glob('content/pages/*_GENERATED_by_add_links.md') \
                      + glob.glob('stubs/*_GENERATED_by_add_links.md')
    
    if args.clean_generated_files:
        for fn in generated_files:
            print('Removing generated file: {}'.format(fn))
            os.remove(fn)
    else:
        print('Reading link file: {}'.format(link_filename))
        with open(link_filename, 'r') as f:
            link_lines = f.readlines()

        for fn in ipython_files:
            make_content_file_from_ipynb(fn, link_lines) 
        for fn in markdown_files:
            make_content_file_from_stub(fn, link_lines)
           
def convert_ipython_files(args):


    generated_files = glob.glob('content/*_GENERATED_by_add_links.md') 
    
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
    convert_files(args)
