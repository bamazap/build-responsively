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
    <!--[if lt IE 9]>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.3/\
html5shiv.js"></script>
    <![endif]-->
</head>
<body style="margin: 0;">
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


def id_div(id, content):
    return '<div id="{}">\n{}</div>\n'.format(id, content)

def build_page_html(name, widgets):
    body = ''.join(map(lambda w: id_div(w['name'], w['html']), widgets))
    return page.format(name, body)

def css_for_widget(widget, clear, width):
    return widget_css.format(widget['name'], clear, width, *widget['width'])

# outputs a css string and an integer number of pixels for the next breakpoint
def css_for_breakpoint(widgets, breakpoint, positions):
    css = '@media screen and (min-width: {}px) {{\n'.format(breakpoint)
    for widget, position in zip(widgets, positions):
        clear = 'left' if position[0] == 0 else 'none'
        width = 100 * min(widget['width'][0] / breakpoint, 1)
        css += css_for_widget(widget, clear, width)
    css += '}\n'
    return css

def build_page_css(widgets):
    layouts = find_breakpoints(widgets, float('inf'))
    css = ''
    for i in range(len(layouts)):
        css += css_for_breakpoint(widgets, *layouts[i])
    return css

def build_page_html_and_css(name, widgets):
    html = build_page_html(name, widgets)
    css = build_page_css(widgets)
    return html, css
