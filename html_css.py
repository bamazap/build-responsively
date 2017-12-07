from layout import find_breakpoints
from name_counter import NameCounter

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
def name_to_id(parent, child, nc, inc=True):
    name = '{}-{}'.format(parent['name'], child['name'])
    count = nc.count(name) if inc else nc.get_count(name)
    return '{}-{}-{}'.format(parent['name'], child['name'], count)

def build_page_html(page, nc=None):
    nc = NameCounter() if nc is None else nc
    widget_html = build_widget_html(page, nc)
    return page_template.format(page['name'], widget_html)

def build_widget_html(widget, nc=None):
    nc = NameCounter() if nc is None else nc
    html = ''
    for child in widget['children']:
        div_id = name_to_id(widget, child, nc)
        html += '<div id="{}">\n{}</div>\n'.format(div_id, child['html'])
    return html

def css_for_widget(parent, widget, clear, width, nc):
    div_id = name_to_id(parent, widget, nc)
    return widget_css.format(div_id, clear, width, *widget['width'])

def css_for_parent(par_id, max_width):
    return parent_css.format(par_id, max_width)

# generates css for the breakpoint based on layout
def css_for_layout(widget, layout, par_id, w_range, scale, nc=None):
    nc = NameCounter() if nc is None else nc
    min_width = round(w_range[0]/scale)
    css = '@media screen and (min-width: {}px) {{\n'.format(min_width)
    child_data = []
    # css to position and size chidlren
    for child, position in zip(widget['children'], layout):
        clear = 'left' if position[0] == 0 else 'none'
        w_frac = min(child['width'][0] / w_range[0], 1) #TODO: revisit
        css += css_for_widget(widget, child, clear, 100*w_frac, nc)
        child_id = name_to_id(widget, child, nc, False)
        child_data.append((child_id, w_frac))
    # don't allow parent to expand past children
    if par_id:
        width_fn = lambda x: x[0]['width'][1] + x[1][0]
        max_width = max(map(width_fn, zip(widget['children'], layout)))
        css += css_for_parent(par_id, max_width)
    css += '}\n'
    # recurse
    for child, (child_id, w_frac) in zip(widget['children'], child_data):
        if child['children']:
            new_w_range = tuple(round(x*scale) for x in w_range)
            css += build_css(child, child_id, new_w_range, scale*w_frac)
    return css

# runs layout algorithm over width-span of widget to find layout breakpoints
# generates css for each layout
# w_range is the minimum and maximum parent width to consider
# scale is the fraction of screen size we are currently at (just to pass thru)
def build_css(widget, par_id=None, w_range=None, scale=1.0):
    w_range = widget['width'] if w_range is None else w_range
    print (w_range, scale)
    # clip to theoretical min/max size and context-dependent size range
    min_width = max(widget['width'][0], w_range[0])
    max_width = min(widget['width'][1], w_range[1])
    children = widget['children']
    max_height = widget['height'][1]
    layouts = find_breakpoints(children, max_height, min_width, max_width)
    css = ''
    for i, (range_min, layout) in enumerate(layouts):
        range_max = max_width if i == len(layouts)-1 else layouts[i+1][0]-1
        print(widget['name'], range_min, range_max, scale, round(range_min/scale), end='')
        if range_min <= range_max:
            print(' used')
            new_w_range = (range_min, range_max)
            css += css_for_layout(widget, layout, par_id, new_w_range, scale)
    return css

# produces css with 100% width and min/max widths for all widgets
# this is necessary for when screen is smaller than all breakpoints
def build_default_css(widget, nc=None):
    nc = NameCounter() if nc is None else nc
    css = ''
    for child in widget['children']:
        child_id = name_to_id(widget, child, nc)
        css += default_css.format(child_id, *child['width'])
        if child['children']:
            css += build_default_css(child, nc)
    return css

def build_page_html_and_css(page):
    html = build_page_html(page)
    css = build_default_css(page) + build_css(page)
    return html, css
