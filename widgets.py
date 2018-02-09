# calculates the minimum and maximum possible widths and heights
# for a generated widget based on the sizes of its children
def calculate_sizes(widget):
    min_width = max([w['width'][0][0] for w in widget['children']])
    max_width = sum([w['width'][-1][1] for w in widget['children']])
    height = sum([w['height'] for w in widget['children']])
    return [min_width, max_width], height

# returns a copy of widget
# this copy has an 'id' field which is unique from all other calls to uniqify
# its children are also unqified
def uniqify(widget, d={}):
    w = widget.copy()
    d[w['name']] = d.get(w['name'], 0) + 1
    w['id'] = '{}-{}'.format(w['name'], d[w['name']])
    if w['children']:
        w['children'] = [uniqify(c, d) for j, c in enumerate(w['children'])]
    return w

# prints the names of the widget and its children in a tree fashion
def print_widget_tree(widget, level=0):
    print(level*'  ' + widget['name'])
    for child in widget['children']:
        print_widget_tree(child, level+1)
