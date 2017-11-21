from argparse import ArgumentParser

from fileio import parse_files, init_build_dir, write_html_css, find_json_file
from sort_group import sort_and_group_widgets
from html_css import build_page_html_and_css

# allow user to pass in JSON file name
parser = ArgumentParser(description='Build HTML and CSS.')
parser.add_argument('--json', type=str,
    help='The JSON file specifying the build.')
args = parser.parse_args()

# use the only JSON file in the current directory if the name is not passed in
json_filename = args.json if args.json else find_json_file()

# read files to get widgets
widgets = parse_files(json_filename)

# set up build directory
init_build_dir()

# base, intermediate, page -- topologically sorted (by children) widgets
b_widgets, i_widgets, p_widgets = sort_and_group_widgets(widgets)

# nothing needs to be done for base widgets

# TODO: support intermediate widgets
if len(i_widgets) > 0:
    raise NotImplementedError

for widget in p_widgets:
    html, css = build_page_html_and_css(widget, widgets)
    write_html_css(widget['name'], html, css)
