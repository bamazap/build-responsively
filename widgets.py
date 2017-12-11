def calculate_sizes(widget):
    min_width = max(map(lambda w: w['width'][0], widget['children']))
    max_width = sum(map(lambda w: w['width'][1], widget['children']))
    min_height = max(map(lambda w: w['height'][0], widget['children']))
    max_height = sum(map(lambda w: w['height'][1], widget['children']))
    return (min_width, max_width), (min_height, max_height)

def uniqify(widget, d={}):
    w = widget.copy()
    d[w['name']] = d.get(w['name'], 0) + 1
    w['name'] += '-{}'.format(d[w['name']])
    if w['children']:
        w['children'] = [uniqify(c, d) for j, c in enumerate(w['children'])]
    return w

def print_widget_tree(widget, level=0):
    print(level*'  ' + widget['name'])
    for child in widget['children']:
        print_widget_tree(child, level+1)
