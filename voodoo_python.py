from os.path import join, dirname, basename
from voodoo import render_skeleton, prompt
from os import system


default_context = {
    'author': 'Virantha N. Ekanayake',
    'author_email': 'virantha@gmail.com',
    'github_username': 'virantha',
    'copyright_year': '2014',
    'description': 'Something like this!',
}

SKELETON_PATH = join(dirname(__file__), "templates", "python_pkg")

def new_project(path, options):
    data = default_context.copy()
    data['project_name'] = prompt("Project name", basename(path))
    data['project_title'] = prompt("Project title", data['project_name'])
    render_skeleton(SKELETON_PATH, path, data=data, **options)
    return data


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Create a new project')
    parser.add_argument('path', help='The name or fullpath of the new project')
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
    full_context = new_project(da.pop('path'), da)

    # Now, make the first_setup zsh script executable
    system('chmod a+x %(project_name)s/first_setup.zsh' % full_context)

