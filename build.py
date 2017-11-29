from argparse import ArgumentParser
import itertools

from fileio import parse_files, init_build_dir, write_html_css, find_json_file
from sort_group import sort_and_group_widgets
from html_css import build_page_html_and_css, build_widget_html

# allow user to pass in JSON file name
parser = ArgumentParser(description='Build HTML and CSS.')
parser.add_argument('--json', type=str,
    help='The JSON file specifying the build.')
args = parser.parse_args()

# use the only JSON file in the current directory if the name is not passed in
json_filename = args.json if args.json else find_json_file()

# read files to get widgets
widgets, user_styles = parse_files(json_filename)

# set up build directory
init_build_dir()

# base, intermediate, page -- topologically sorted (by children) widgets
b_widgets, i_widgets, p_widgets = sort_and_group_widgets(widgets)

# nothing needs to be done for base widgets

# calculate sizes for generated widgets
for widget in itertools.chain(i_widgets, p_widgets):
    min_width = max(map(lambda w: w['width'][0], widget['children']))
    max_width = sum(map(lambda w: w['width'][1], widget['children']))
    height = sum(map(lambda w: w['height'][0], widget['children']))
    widget['width'] = (min_width, max_width)
    widget['height'] = (height, height)

# generate HTML for intermediate widgets
for widget in i_widgets:
    widget['html'] = build_widget_html(widget)

# generate HTML and CSS for pages
for widget in p_widgets:
    html, css = build_page_html_and_css(widget)
    write_html_css(widget['name'], html, user_styles + css)
