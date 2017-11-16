import os
import json
from argparse import ArgumentParser
from shutil import rmtree
from toposort import toposort_flatten

# allow user to pass in JSON file name
parser = ArgumentParser(description='Build HTML and CSS.')
parser.add_argument('--json', type=str,
    help='The JSON file specifying the build.')
args = parser.parse_args()
json_filename = args.json

# use the only JSON file if the name is not passed in
if not json_filename:
    json_files = [f for f in os.listdir('.') if f.endswith('.json')]
    if len(json_files) != 1:
        raise FileNotFoundError('Did not find a single JSON file in this \
            directory. Please give the file name as an argument.')
    json_filename = json_files[0]

# read the JSON file
widgets = {}
with open(json_files[0]) as f:
    data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError('JSON file is not formatted properly.')
    widgets = data

# set up an empty build folder
try:
    rmtree('build')
except FileNotFoundError:
    pass
os.makedirs('build')

# get sizes and content of the base widgets
# TODO: handle more than just fixed sizes
# TODO: figure out whose job it is to enforce sizes
num_base_widgets = 0
for root, dirs, files in os.walk('src'):
    for name in files:
        if name.endswith('.html'):
            with open(os.path.join(root, name)) as f:
                size_comment = f.readline()
                size_comment = size_comment.replace('<!--', '{')
                size_comment = size_comment.replace('-->', '}')
                size = json.loads(size_comment)
                widget_name = name.split('.')[0]
                if widget_name in widgets:
                    raise FileExistsError('HTML provided for widget in JSON \
                        file.')
                widgets[name.split('.')[0]] = {
                    'width': size['width'],
                    'height': size['height'],
                    'html': f.read(),
                    'children': []
                }
                num_base_widgets += 1

# add a 'name' field to each widget (makes things easier later)
for widget_name, widget_properties in widgets.items():
    widget_properties['name'] = widget_name

# given a list of widgets
# output a list of position tuples (x, y)
def assign_positions(widgets, width, height):
    positions = []
    x = 0
    y = 0
    row_height = 0
    for widget in widgets:
        if x + widget['width'] > width:
            x = 0
            y += row_height
            row_height = 0
        positions.append((x, y))
        row_height = max(row_height, widget['height'])
        x += widget['width']
    return positions

# does assign_positions at every width in the range
# outputs a list of tuples (width, layout)
# layout is position assignments like in assign_positions
# the layout should be used for all parent sizes > width (overriding last one)
def find_breakpoints(widgets, height, min_width=300, max_width=2000):
    breakpoints = [(300, assign_positions(widgets, min_width, height))]
    for width in range(min_width+1, max_width+1):
        next_layout = assign_positions(widgets, width, height)
        if next_layout != breakpoints[-1][1]:
            breakpoints.append((width, next_layout))
    return breakpoints

# heading info to be put in all pages
page_head = '''\
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{0}</title>
  <meta name="description" content="{1}">
  <meta name="author" content="{2}">
  <meta name="viewport" content="width=device-width">
  <link rel="stylesheet" href="{0}.css?v=1.0">
  <!--[if lt IE 9]>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.3/\
html5shiv.js"></script>
  <![endif]-->
</head>
<body>
  {3}
</body>
</html>
'''

pos_css = '''  #{} {{
    left: {}px;
    top: {}px;
  }}
'''

# given a widget, build HTML for it
def build_page_html_and_css(widget):
    child_widgets = tuple(map(lambda cn: widgets[cn], widget['children']))
    html = '<div style="position: relative;">\n'
    for child_name in widget['children']:
        html += '<div id={} style="position: absolute;">\n'.format(child_name)
        html += widgets[child_name]['html'] + '\n'
        html += '</div>\n'
    html += '</div>'
    layouts = find_breakpoints(child_widgets, float('inf'))
    css = ''
    for breakpoint, layout in layouts:
        css += '@media screen and (min-width: {}px) {{\n'.format(breakpoint)
        for widget_name, position in zip(widget['children'], layout):
            css += pos_css.format(widget_name, position[0], position[1])
        css += '}\n'
    page_html = page_head.format(widget['name'], 'desc', 'auth', html)
    return page_html, css

# build HTML
# TODO: actually do something intelligent
# TODO: consider widgets which contain other widgets and are used in pages
hopefully_dag = {}
for widget_name, widget_properties in widgets.items():
    hopefully_dag[widget_name] = set(widget_properties['children'])
for widget_name in toposort_flatten(hopefully_dag)[num_base_widgets:]:
    widget = widgets[widget_name]
    html, css = build_page_html_and_css(widget)
    with open('build/{}.html'.format(widget_name), 'w+') as f:
        f.write(html)
    with open('build/{}.css'.format(widget_name), 'w+') as f:
        f.write(css)


# figure out which widgets are contained within other widgets
# all_children = {}
# for widget_properties in widgets.values():
#     for child in widget_properties['children']:
#         all_children.add(child)
