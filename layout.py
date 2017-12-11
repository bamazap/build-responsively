# naive layout algorithm
# given a list of widgets
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
        if x + widget['width'][0] > width:
            x = 0
            y += row_height
            row_height = 0
            max_w = max(max_x, max_w)
            max_x = 0
        positions.append((x, y))
        row_height = max(row_height, widget['height'][0])
        x += widget['width'][0]
        max_x += widget['width'][1]
    return positions, max(max_x, max_w)

# returned is a multiple_layout: a list of (min-width, layout, max-width) tuples
# min-width means that this layout should activate when there are at least
#   min-width pixels of space (overriding any layouts with smaller min-width)
# layout spec described in spec for single_layout
# max-width means that this layout will not take up more than max-width pixels
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


