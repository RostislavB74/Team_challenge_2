from django import template

register = template.Library()

@register.inclusion_tag('navigation/menu_tree.html')
def render_menu(menu_items):
    return {'menu_items': menu_items}
