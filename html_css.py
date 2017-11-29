from layout import find_breakpoints
from name_counter import NameCounter
import math

page_template = '''\
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{0}</title>
    <meta name="viewport" content="width=device-width">
    <link rel="stylesheet" href="{0}.css?v=1.0">
</head>
<body style="margin:0;">
    {1}
</body>
</html>
'''

widget_css = '''  #{} {{
    float: left;
    clear: {};
    width: {}%;
    min-width: {}px;
    max-width: {}px;
  }}
'''

parent_css = '''  #{} {{
    max-width: {}px;
  }}
'''

default_css = '''#{} {{
  width: 100%;
  min-width: {}px;
  max-width: {}px;
}}
'''

# get the correct id for a widget, update name_counts
def name_to_id(parent, child, name_counter, inc=True):
    name = '{}-{}'.format(parent['name'], child['name'])
    count = name_counter.count(name) if inc else name_counter.get_count(name)
    return '{}-{}-{}'.format(parent['name'], child['name'], count)

def build_page_html(page, name_counter=None):
    name_counter = NameCounter() if name_counter is None else name_counter
    widget_html = build_widget_html(page, name_counter)
    return page_template.format(page['name'], widget_html)

def build_widget_html(widget, name_counter=None):
    name_counter = NameCounter() if name_counter is None else name_counter
    html = ''
    for child in widget['children']:
        div_id = name_to_id(widget, child, name_counter)
        html += '<div id="{}">\n{}</div>\n'.format(div_id, child['html'])
    return html

def css_for_widget(parent, widget, clear, width, name_counter):
    div_id = name_to_id(parent, widget, name_counter)
    return widget_css.format(div_id, clear, width, *widget['width'])

def css_for_parent(parent_id, max_width):
    return parent_css.format(parent_id, max_width)

def css_for_layout(widget, layout, scale, parent_id, name_counter=None):
    name_counter = NameCounter() if name_counter is None else name_counter
    css = '@media screen and (min-width: {}px) {{\n'.format(scale*layout[0])
    child_ids = []
    for child, position in zip(widget['children'], layout[1]):
        clear = 'left' if position[0] == 0 else 'none'
        w_frac = min(child['width'][0] / layout[0], 1)
        css += css_for_widget(widget, child, clear, 100*w_frac, name_counter)
        child_ids.append(name_to_id(widget, child, name_counter, False))
    if parent_id:
        width_fn = lambda x: x[0]['width'][1] + x[1][0]
        max_width = max(map(width_fn, zip(widget['children'], layout[1])))
        css += css_for_parent(parent_id, max_width)
    css += '}\n'
    for child, child_id in zip(widget['children'], child_ids):
        if child['children']:
            css += build_css(child, scale/w_frac, child_id)
    return css

def build_css(widget, scale=1, parent_id=None):
    children = widget['children']
    max_height = widget['height'][1]
    layouts = find_breakpoints(children, max_height, *widget['width'])
    css = ''
    for layout in layouts:
        css += css_for_layout(widget, layout, scale, parent_id)
    return css

def build_default_css(widget, name_counter=None):
    name_counter = NameCounter() if name_counter is None else name_counter
    css = ''
    for child in widget['children']:
        child_id = name_to_id(widget, child, name_counter)
        css += default_css.format(child_id, *child['width'])
        for grandchild in child['children']:
            css += build_default_css(grandchild, name_counter)
    return css


def build_page_html_and_css(page):
    html = build_page_html(page)
    css = build_default_css(page) + build_css(page)
    return html, css
