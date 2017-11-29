from toposort import toposort_flatten

# topologically sorts the widgets and breaks them up into categories
# base widgets: has no children
# intermediate widgets: has children and is contained by another widget
# page widgets: has children and is contained by no other widgets
def sort_and_group_widgets(widgets):
    # make set of names of all widgets which are children
    all_children = set()
    for widget_properties in widgets.values():
        for child in widget_properties['children']:
            all_children.add(child['name'])
    # make dictionary mapping parent name to child names
    hopefully_dag = {}
    for widget_name, widget_properties in widgets.items():
        child_names = map(lambda c: c['name'], widget_properties['children'])
        hopefully_dag[widget_name] = set(child_names)
    base_widgets = []
    intermediate_widgets = []
    page_widgets = []
    for widget_name in toposort_flatten(hopefully_dag):
        if len(widgets[widget_name]['children']) == 0:
            base_widgets.append(widgets[widget_name])
        elif widget_name in all_children:
            intermediate_widgets.append(widgets[widget_name])
        else:
            page_widgets.append(widgets[widget_name])
    return base_widgets, intermediate_widgets, page_widgets
