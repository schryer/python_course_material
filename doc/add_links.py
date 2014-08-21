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

def convert_ipynb_file_to_stub(ipynb_path):

    notebook_filename = os.path.split(ipynb_path)[-1]
    generation_directory = 'stubs/notebooks/generated/'
    notebook_directory = 'content/notebooks/'
    notebook_path = ipynb_path.replace('stubs/notebooks/', notebook_directory)
    generated_path = ipynb_path.replace('stubs/notebooks/', generation_directory).replace('.ipynb', '_GENERATED_by_add_links.ipynb')
    generated_md_path = generated_path.replace('.ipynb', '.md')
    stub_md_path = generated_path.replace('.ipynb', '_stub.md')
    final_md_path = stub_md_path.replace(generation_directory, 'content/')
        
    # Copy original files to generated directory    
    original_meta_path = ipynb_path.replace('.ipynb', '.ipynb-meta')
    generated_meta_path = generated_path.replace('.ipynb', '.ipynb-meta')
    
    cmd = 'cp {} {}'.format(original_meta_path, generated_meta_path)
    print('Executing: {}'.format(cmd))
    os.system(cmd)

    cmd = 'cp {} {}'.format(ipynb_path, generated_path)
    print('Executing: {}'.format(cmd))
    os.system(cmd)

    # Copy original ipynb files to content/notebooks
    cmd = 'cp {} {}'.format(ipynb_path, notebook_path)
    print('Executing: {}'.format(cmd))
    os.system(cmd)
    
    # Convert ipynb files within generated directory
    support_path = generated_path.replace('.ipynb', '_files')
    support_directory = os.path.split(support_path)[-1]
    generated_filename = os.path.split(generated_path)[-1]
    
    cwd = os.getcwd()
    print('Changing working directory to: {}'.format(generation_directory))
    os.chdir(generation_directory)
    
    cmd = 'ipython nbconvert --to markdown {}'.format(generated_filename)
    print('Executing: {}'.format(cmd))
    os.system(cmd)
    
    print('Changing working directory back to: {}'.format(cwd))
    os.chdir(cwd)

    # A: Write final .md file and B: move support files to images directory
    glob_str = '{}/*'.format(support_path)
    support_files = glob.glob(glob_str)
        
    # A: Write final .md file

    download_text = '![{0}]({{filename}}/notebooks/{0})'.format(notebook_filename)
    
    print('Reading generated Markdown file: {}'.format(generated_md_path))
    with open(generated_md_path, 'r') as f:
        md_lines = f.readlines()

    print('Reading: {}'.format(generated_meta_path))
    with open(generated_meta_path, 'r') as f:
        meta_lines = f.readlines()

    print('Writing stub Markdown file: {}'.format(stub_md_path))
    support_files_found = []
    with open(stub_md_path, 'w') as f:
        for line in meta_lines:
            f.write(line)

        f.write('Download original file: {}\n'.format(download_text))
            
        for line_number, line in enumerate(md_lines):
            if len(line.split(support_directory)) > 1:
                line = line.replace(support_directory, 'images')
                
                found = False
                for support_file in support_files:
                    base_filename = os.path.split(support_file)[-1]
                    if len(line.split(base_filename)) > 1:
                        print('Replacing support file {} on Markdown line {} to: {}'.format(base_filename, line_number, line))
                        support_files_found.append(support_file)
                        found = True

                if not found:
                    raise Exception('Something is wrong with this support file reference on line number {}'.format(line_number),
                                    (line, support_directory))
            f.write(line)

    if len(support_files_found) != len(support_files):
        raise Exception('Not all support files were found.', (support_files, support_files_found, generated_path))                        
                
    # C: move support files to images directory
    for support_file in support_files:
        base_filename = os.path.split(support_file)[-1]
        image_filename = 'content/images/{}'.format(base_filename)
        cmd = 'cp {} {}'.format(support_file, image_filename)
        print('Moving supporting image using: {}'.format(cmd))
        os.system(cmd)

    return stub_md_path, final_md_path

    
def make_content_file_from_stub(stub_filename, generated_filename, link_filename='external_links.md'):

    print('Reading stub file: {}'.format(stub_filename))
    with open(stub_filename, 'r') as f:
        stub_lines = f.readlines()

    print('Reading link file: {}'.format(link_filename))
    with open(link_filename, 'r') as f:
        link_lines = f.readlines()
        
    print('Adding links and making content file: {}'.format(generated_filename))
    with open(generated_filename, 'w') as f:
        for line in stub_lines + ['\n', '\n'] + link_lines:
            f.write(line)

def process_arguments(args):

    markdown_files = glob.glob('stubs/*.md') + glob.glob('stubs/pages/*.md')
    ipynb_files = glob.glob('stubs/notebooks/*.ipynb')
    ipynb_meta_files = glob.glob('stubs/notebooks/*.ipynb-meta')
    
    generated_files = glob.glob('content/*_GENERATED_by_add_links.md') \
                      + glob.glob('content/pages/*_GENERATED_by_add_links.md') \
                      + glob.glob('content/notebooks/*.ipynb') 
    
    if args.clean_generated_files:
        for gfn in generated_files:
            print('Removing generated file: {}'.format(gfn))
            os.remove(gfn)
    else:    
        for stub in markdown_files:
            generated_filename = stub.replace('stubs/', 'content/').replace('.md', '_GENERATED_by_add_links.md')
            make_content_file_from_stub(stub, generated_filename)

        converted_ipynb_files = []
        for meta_file in ipynb_meta_files:

            ipynb_file = meta_file.replace('.ipynb-meta', '.ipynb')

            if ipynb_file not in ipynb_files:
                print('WARNING: An IPython notebook metadata file was found without its partner: {}'.format(meta_file))
                continue

            stub_path, final_path = convert_ipynb_file_to_stub(ipynb_file)
            make_content_file_from_stub(stub_path, final_path)
            converted_ipynb_files.append(ipynb_file)

        # Check if all IPython notebook files had metadata files:
        for ipynb_file in ipynb_files:
            if ipynb_file not in converted_ipynb_files:
                print('WARNING: An IPython notebook file was found without its partner IPython notebook metadata file: {}'.format(ipynb_file))
            
if __name__ == '__main__':
    p = make_argument_parser()
    args = p.parse_args()
    process_arguments(args)
