from os.path import join, dirname, basename
from voodoo import render_skeleton, prompt
from os import system
import os
import yaml


default_context = {
    'author': 'Virantha N. Ekanayake',
    'author_email': 'virantha@gmail.com',
    'github_username': 'virantha',
    'copyright_year': '2014',
    'description': 'Something like this!',
}

SKELETON_PATH = join(dirname(__file__), "templates", "python_pkg")

def get_merged_dict(x,y):
    z = x.copy()
    z.update(y)
    return z

def new_project(path, options):
    data = default_context.copy()

    yaml_filename = options.pop('config')
    print("Loading configuration from %s" % yaml_filename)
    with open(yaml_filename) as f:
        config_dict = yaml.load(f)

    data = get_merged_dict(data, config_dict)    
    #data['project_name'] = prompt("Project name", basename(path))
    #data['project_title'] = prompt("Project title", data['project_name'])
    render_skeleton(SKELETON_PATH, path, data=data, **options)
    return data


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Create a new project')
    parser.add_argument('path', help='The name or fullpath of the new project')
    parser.add_argument('config', help='The configuration yaml for the project')

    parser.add_argument('-p', '--pretend', action='store_true',
                        help='Run but do not make any changes')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Overwrite files that already exist, without asking')
    parser.add_argument('-s', '--skip', action='store_true',
                        help='Skip files that already exist, without asking')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Suppress status output')

    args = parser.parse_args()
    da = vars(args)
    proj_path = da.pop('path')
    full_context = new_project(proj_path, da)

    # Now, make the first_setup zsh script executable
    full_context['path'] = proj_path
    system('chmod a+x %(path)s/first_setup.zsh' % full_context)

