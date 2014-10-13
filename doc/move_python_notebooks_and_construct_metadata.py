import os
from collections import namedtuple, OrderedDict

def fill_template(ordered_dictionary, template_string):
    _NT = namedtuple('_NT', ordered_dictionary.keys())
    nt = _NT(*ordered_dictionary.values())
    return template_string.format(nt)

meta_tmpl = '''Title: {0.title}
Date: {0.year}-{0.month}-{0.day} {0.time}
Tags: {0.tags}
URL: python/{0.urlname}.html
save_as: python/{0.urlname}.html
Category: page
Slug: python/{0.urlname}
Author: David Schryer
Summary: {0.summary}

'''

index_dic = OrderedDict([('filename', 'generated'),
                         ('title', 'Index of Python notebook pages'),
                         ('year', '2014'),
                         ('month', '09'),
                         ('day', '02'),
                         ('time', '9:00'),
                         ('tags', 'python, ipython'),
                         ('urlname', 'index'),
                         ('summary', 'List of Python notebooks used in the course.'),
                     ])

def make_python_subjects(base_dictionary):

    python_1 = dict(base_dictionary)
    python_1.update(dict(filename='../topics/python/1_reading_python_code.ipynb',
                         title='Python is not a natural language',
                         urlname='python_1',
                         summary='Explains that Python must be read differently than natural languages.',
                     ))

    python_2 = dict(base_dictionary)
    python_2.update(dict(filename='../topics/python/2_fundamental_python_types.ipynb',
                         title='Fundamental types in Python',
                         urlname='python_2',
                         summary='Presents a few fundamental types in Python.',
                     ))

    python_3 = dict(base_dictionary)
    python_3.update(dict(filename='../topics/python/3_python_strings_as_containers.ipynb',
                         title='Introducing containers in Python',
                         urlname='python_3',
                         summary='Introduces what we can do with containers in Python.'
                     ))

    python_4 = dict(base_dictionary)
    python_4.update(dict(filename='../topics/python/4_python_keywords.ipynb',
                         title='Keywords, __builtin__, and the Python standard library',
                         urlname='python_4',
                         summary='Introduces the global Python namespace.'
                     ))

    python_5 = dict(base_dictionary)
    python_5.update(dict(filename='../topics/python/5_elementwise_and_vector_operations.ipynb',
                         title='Elementwise and vector operations in Python',
                         urlname='python_5',
                         summary='Introduces elementwise and vector operations in Python using NumPy and pandas.'
                     ))
    python_6 = dict(base_dictionary)
    python_6.update(dict(filename='../topics/python/6_functions_with_tests.ipynb',
                         title='Functions that use Biopython objects together with tests.',
                         urlname='python_6',
                         summary='Working version of the functions we wrote together in class.'
                     ))
    python_7 = dict(base_dictionary)
    python_7.update(dict(filename='../topics/python/7_introduction_to_sequence_alignment_Entrez_and_curve_fitting.ipynb',
                         title='Introduction to sequence alignment, Entrez database retrieval and curve fitting.',
                         urlname='python_7',
                         summary='Some odd topics that could be useful.'
                     ))    

    return [python_1, python_2, python_3, python_4, python_5, python_6, python_7]


def move_python_notebooks_and_construct_metadata(index_dic, meta_template):

    subjects = make_python_subjects(index_dic)

    # Make python content index file
    index_header = fill_template(index_dic, meta_template).replace('Slug: python/index', 'Slug: python')
    index_path = 'stubs/pages/python_index.md'
    print('Creating python directory index file: {}'.format(index_path))
    with open(index_path, 'w') as f:
        f.write(index_header)

        for subject_dic in subjects:
            urlname = subject_dic['urlname']
            summary = subject_dic['summary']
            original_path = subject_dic['filename']
            original_dir, original_fn = os.path.split(original_path)
            content_fn = original_fn.replace('.ipynb', '_GENERATED_by_add_links_stub.md')
            f.write('* [python/{}]({{filename}}/pages/{}): {}\n'.format(urlname, content_fn, summary))
        f.write('\n\n')

    # Move original ipynb files to stub location
    # and make meta files that are used to generate
    # the .md files in the content directory.
    for subject_dic in subjects:
        original_path = subject_dic['filename']
        original_dir, original_fn = os.path.split(original_path)
        dest_dir = 'stubs/python/'
        dest_path = os.path.join(dest_dir, original_fn)

        cmd = 'cp {} {}'.format(original_path, dest_path)
        print('Moving notebook file to stub directory by Executing: {}'.format(cmd))
        os.system(cmd)

        meta_fn = original_fn.replace('.ipynb', '.ipynb-meta')
        meta_path = os.path.join(dest_dir, meta_fn)

        print('Creating ipynb meta file: {}'.format(meta_path))
        with open(meta_path, 'w') as f:
            f.write(fill_template(subject_dic, meta_template))

            
if __name__ == '__main__':
    
    move_python_notebooks_and_construct_metadata(index_dic, meta_tmpl)