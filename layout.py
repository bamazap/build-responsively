# given a list of widgets
# output a list of position tuples (x, y)
def assign_positions(widgets, width, height):
    positions = []
    x = 0
    y = 0
    row_height = 0
    for widget in widgets:
        if x + widget['width'][0] > width:
            x = 0
            y += row_height
            row_height = 0
        positions.append((x, y))
        row_height = max(row_height, widget['height'])
        x += widget['width'][0]
    return positions

# does assign_positions at every width in the range
# outputs a list of tuples (width, layout)
# layout is position assignments like in assign_positions
# the layout should be used for all parent sizes > width (overriding last one)
def find_breakpoints(widgets, height, min_width=300, max_width=2000):
    breakpoints = [(300, assign_positions(widgets, min_width, height))]
    for width in range(min_width+1, max_width+1):
        next_layout = assign_positions(widgets, width, height)
        if next_layout != breakpoints[-1][1]:
            breakpoints.append((width, next_layout))
    return breakpoints
