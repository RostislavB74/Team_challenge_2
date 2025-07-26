from django import template
from navigation.models import MenuItem

register = template.Library()

@register.inclusion_tag('navigation/menu.html', takes_context=True)
def render_menu(context):
    user = context['request'].user
    sql_role = getattr(user, 'sql_role', None)

    items = MenuItem.objects.filter(parent__isnull=True, visible=True).order_by('order')
    menu = []

    for item in items:
        if item.is_allowed_for(sql_role):
            children = item.children.filter(visible=True).order_by('order')
            menu.append({
                'item': item,
                'children': [child for child in children if child.is_allowed_for(sql_role)]
            })

    return {'menu': menu}
