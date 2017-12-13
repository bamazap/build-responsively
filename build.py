from argparse import ArgumentParser
import itertools
from json import dumps as to_json

from fileio import *
from sort_group import sort_and_group_widgets
from html_css import build_page_html, build_widget_html, build_page_css
from layout import multiple_layouts
from widgets import calculate_sizes, uniqify, print_widget_tree

# allow user to pass in JSON file name
parser = ArgumentParser(description='Build HTML and CSS.')
parser.add_argument('--json', type=str,
    help='The JSON file specifying the build.')
args = parser.parse_args()

# use the only JSON file in the current directory if the name is not passed in
json_filename = args.json if args.json else find_json_file()

# read json file and html files to get widgets
widgets = parse_json_file(json_filename)

# get contents of user-provided css files
user_styles = get_user_css()

head = get_head()

# set up build directory
init_build_dir()

# base, intermediate, page -- topologically sorted (by children) widgets
b_widgets, i_widgets, p_widgets = sort_and_group_widgets(widgets)

# calculate size ranges for generated widgets
for w in itertools.chain(i_widgets, p_widgets):
    w['width'], w['height'] = calculate_sizes(w)
    w['layouts'] = multiple_layouts(w, w['width'], w['height'])

# generate HTML and CSS for pages
for widget in p_widgets:
    page = uniqify(widget)
    html = build_page_html(page, json_filename[:-5], head)
    css = build_page_css(page)
    write_html_css(page['name'], html, user_styles + css)
