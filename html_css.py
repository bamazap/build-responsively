# contains page head, allowing info and html body to be injected
page_template = '''\
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{1} | {0}</title>
    <meta name="viewport" content="width=device-width">
    <link rel="stylesheet" href="{0}.css?v=1.0">
    {2}
</head>
<body style="margin:0;">
    {3}
</body>
</html>
'''

# used to resize & reposition widgets at breakpoints
widget_css = '''  #{} {{
    clear: {};
    width: {}%;
    min-width: {}px;
    max-width: {}px;
  }}
'''

# prevent parents from expanding past their children
parent_css = '''  #{} {{
    max-width: {}px;
  }}
'''

# when screen is smaller than all breakpoints, stack widgets at 100% size
default_css = '''#{} {{
  width: 100%;
  float: left;
  min-width: {}px;
  max-width: {}px;
  height: {}px;
}}
'''

# a simple div tag, with space for id, class, and children
div_html = '<div id="{}" class="{}">\n{}</div>\n'

# concatenates the html of the widget's children and returns it
# or returns the value of the html field for a base widget
def build_widget_html(widget):
    if 'html' in widget:
        return widget['html']
    w_html = ''
    for c in widget['children']:
        c_html = build_widget_html(c)
        w_html += div_html.format(c['id'], c['name'], c_html)
    return w_html

# creates html for a page widget, using html of child widgets
def build_page_html(page, app_name, head):
    body = build_widget_html(page)
    return page_template.format(page['name'], app_name, head, body)

# returns css for a widget, given its name & the properties it should have
def css_for_widget(name, clear, per_width, min_width, max_width):
    return widget_css.format(name, clear, per_width, min_width, max_width)

# generates css for the breakpoint based on layout
def css_for_layout(widget, positions, w_range, scale):
    if scale == 0:
        return ''
    breakpoint = round(w_range[0]/scale)
    css = '@media screen and (min-width: {}px) {{\n'.format(breakpoint)
    rest_css = ''
    for child, position in zip(widget['children'], positions):
        # put on new line if x position is 0 (may need to revisit)
        clear = 'left' if position[0] == 0 else 'none'
        # % width based on minimum widths (may need to revisit)
        w_frac = 1 if (child['row'] or w_range[0] == 0) \
            else min(child['width'][0] / w_range[0], 1)
        css += css_for_widget(child['id'], clear, 100*w_frac, *child['width'])
        # recurse
        if child['children']:
            new_w_range = tuple(round(x*scale) for x in w_range)
            rest_css += build_css(child, widget, new_w_range, scale*w_frac)
    css += '}\n'
    return css + rest_css

# runs layout algorithm over width-span of widget to find layout breakpoints
# generates css for each layout
# w_range is the minimum and maximum parent width to consider
# scale is the fraction of screen size we are currently at (just to pass thru)
def build_css(widget, parent=None, w_range=None, scale=1.0):
    css = ''
    for i, (w_range, positions) in enumerate(widget['layouts']):
        # clip max width to next breakpoint
        range_max = w_range[1]
        if (i+1) < len(widget['layouts']):
            range_max = min(range_max, widget['layouts'][i+1][0][0]-1)
        css += css_for_layout(widget, positions, (w_range[0], range_max), scale)
    return css

# produces css with 100% width and min/max widths for all widgets
# this is necessary for when screen is smaller than all breakpoints
def build_default_css(widget):
    css = ''
    for c in widget['children']:
        css += default_css.format(c['id'], *c['width'], c['height'])
        if c['children']:
            css += build_default_css(c)
    return css

# call this entry function on a page widget to get the right css
def build_page_css(page):
    return build_default_css(page) + build_css(page)
