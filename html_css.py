from layout import find_breakpoints

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

elm_css = '''  #{} {{
    left: {}%;
    top: {}px;
    width: {}%;
  }}
'''

# given a widget, build HTML for it
def build_page_html_and_css(widget, widgets):
    child_widgets = tuple(map(lambda cn: widgets[cn], widget['children']))
    html = '<div style="position: relative;">\n'
    for child_name in widget['children']:
        html += '<div id={} style="position: absolute;">\n'.format(child_name)
        html += widgets[child_name]['html']
        html += '</div>\n'
    html += '</div>\n'
    layouts = find_breakpoints(child_widgets, float('inf'))
    css = ''
    for breakpoint, layout in layouts:
        css += '@media screen and (min-width: {}px) {{\n'.format(breakpoint)
        for widget_name, position in zip(widget['children'], layout):
            left = 100 * position[0] / breakpoint
            width = 100 * widgets[widget_name]['width'][0] / breakpoint
            css += elm_css.format(widget_name, left, position[1], width)
        css += '}\n'
    page_html = page_head.format(widget['name'], 'desc', 'auth', html)
    return page_html, css
