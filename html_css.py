from layout import find_breakpoints
import math

page = '''\
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

def id_div(div_id, content):
    return '<div id="{}">\n{}</div>\n'.format(div_id, content)

# maps widget names to number of times it has been added to the page
name_counts = {}
# get the correct id for a widget, update name_counts
def name_to_id(parent_name, child_name):
    name_counts[child_name] = name_counts.get(child_name, 0) + 1
    return '{}-{}-{}'.format(parent_name, child_name, name_counts[child_name])
def reset_name_counts():
    for name in name_counts.keys():
        name_counts[name] = 0

def build_page_html(name, widgets):
    def widget_to_div(widget):
        return id_div(name_to_id(name, widget['name']), widget['html'])
    body = ''.join(map(widget_to_div, widgets))
    return page.format(name, body)

def css_for_widget(name, widget, clear, width):
    div_id = name_to_id(name, widget['name'])
    return widget_css.format(div_id, clear, width, *widget['width'])

# outputs a css string and an integer number of pixels for the next breakpoint
def css_for_breakpoint(name, widgets, breakpoint, positions):
    css = '@media screen and (min-width: {}px) {{\n'.format(breakpoint)
    for widget, position in zip(widgets, positions):
        clear = 'left' if position[0] == 0 else 'none'
        width = 100 * min(widget['width'][0] / breakpoint, 1)
        css += css_for_widget(name, widget, clear, width)
    css += '}\n'
    return css

def build_page_css(name, widgets):
    layouts = find_breakpoints(widgets, float('inf'))
    css = ''
    for i in range(len(layouts)):
        reset_name_counts()
        css += css_for_breakpoint(name, widgets, *layouts[i])
    return css

def build_page_html_and_css(name, widgets):
    html = build_page_html(name, widgets)
    css = build_page_css(name, widgets)
    return html, css
