# naive layout algorithm
# given a list of widgets and the available width and height
# output a list of position tuples (x, y)
# also returns the width of the layout if all widgets expand to max-width
def assign_positions(widgets, width, height):
    positions = []
    x = 0
    y = 0
    row_height = 0
    max_x = 0
    max_w = 0
    for widget in widgets:
        if x + widget['width'][0][0] > width or widget['row']:
            x = 0
            y += row_height
            row_height = 0
            max_w = max(max_x, max_w)
            max_x = 0
        positions.append((x, y))
        row_height = max(row_height, widget['height'])
        x += widget['width'][0][0]
        max_x += widget['width'][-1][1]
        if widget['row']:
            x = 0
            y += row_height
            row_height = 0
            max_w = max(max_x, max_w)
            max_x = 0
    return positions, max(max_x, max_w)

# returned is a multiple_layout: a list of ((min-width, max-width), layout)
# min-width means that this layout should activate when there are at least
#   min-width pixels of space (overriding any layouts with smaller min-width)
# max-width means that this layout will not take up more than max-width pixels
# layout spec described in spec for single_layout
def multiple_layouts(widget, width_range, max_height):
    if not widget['children']:
        return []
    layouts = []
    for width in range(width_range[0], width_range[1]+1):
        layout, maxw = single_layout(widget['children'], width, max_height)
        if len(layouts) == 0 or layout != layouts[-1][1]:
            layouts.append(((width, maxw), layout))
    return layouts

# returned is a layout: a list of (x, y, multiple_layouts) tuples
def single_layout(widgets, width, height):
    positions, maxw = assign_positions(widgets, width, height)
    return positions, maxw

# layout: (layout | boolean)[]
# each boolean corresponds to a child widget, each layout to a group of them
#   the boolean says whether or not the widget starts a new line
#   the first boolean of a layout says if the layout starts a new line
# this particular function uses a single grouping with nls when space runs out
def create_layout(widget, max_width):
    newlines = []
    x = 0
    for child in widget['children']:
        if x + child['width'][0][0] > max_width or child['row']:
            x = 0
            newlines.append(True)
        else:
            newlines.append(False)
        x += widget['width'][0][0]
        if widget['row']:
            x += max_width # forces the next one to be on a new line
    newlines[0] = True
    return [newlines]

def calculate_size_of_layout(widget):
    children = widget['children']
    layout = widget['layout']


def layouts(widget):
    # convert children into layout
    widget['layout'] = create_layout(widget)
    # calculate size of layout