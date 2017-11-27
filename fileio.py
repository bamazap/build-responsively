import os
import json
from shutil import rmtree

# convers [a, b] to (a, b) or a to (a, a)
def size_as_tuple(num_or_list):
    if isinstance(num_or_list, list):
        return tuple(num_or_list)
    return (num_or_list)

# convert the comment specifying the widget size
# returns ((minW, maxW), (minH, maxH))
def parse_size_comment(size_comment):
    size_json = size_comment.replace('<!--', '{').replace('-->', '}')
    size_dict = json.loads(size_json)
    return tuple(size_as_tuple(size_dict[key]) for key in ('width', 'height'))

# given the json file which specifies the app composition
# returns a dictionary of all of the app's widgets
# may fail with an error due to file io
def parse_files(json_filename):
    # read the JSON file
    widgets = {}
    css = ''
    with open(json_filename) as f:
        data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError('JSON file is not formatted properly.')
        widgets = data

    # add a 'name' field to each widget (makes things easier later)
    for widget_name, widget_properties in widgets.items():
         widget_properties['name'] = widget_name

     # get sizes and content of the base widgets
    # TODO: figure out whose job it is to enforce sizes
    num_base_widgets = 0
    for root, dirs, files in os.walk('src'):
        for filename in files:
            if filename.endswith('.html'):
                with open(os.path.join(root, filename)) as f:
                    width, height = parse_size_comment(f.readline())
                    widget_name = filename[:-5]
                    if widget_name in widgets:
                        e_str ='HTML provided for widget in JSON file.'
                        raise FileExistsError(e_str)
                    widgets[widget_name] = {
                        'width': width,
                        'height': height,
                        'html': f.read(),
                        'children': [],
                        'name': widget_name
                    }
            elif filename.endswith('.css'):
                with open(os.path.join(root, filename)) as f:
                    css += f.read()

    return widgets, css

# create a directory named 'build' if it does not exist
# empty the directory if it does
def init_build_dir():
    try:
        rmtree('build')
    except FileNotFoundError:
        pass
    os.makedirs('build')

def write_html_css(filename, html, css):
    with open('build/{}.html'.format(filename), 'w+') as f:
        f.write(html)
    with open('build/{}.css'.format(filename), 'w+') as f:
        f.write(css)

# returns the filename of the only .json file in the current directory
# raises a FileNotFoundError if zero or more than one file was found
def find_json_file():
    json_files = [f for f in os.listdir('.') if f.endswith('.json')]
    if len(json_files) != 1:
        raise FileNotFoundError('Did not find a single JSON file in this \
            directory. Please give the file name as an argument.')
    return json_files[0]
