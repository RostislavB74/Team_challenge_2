from .models import MenuItem
from utils.utils import get_user_sql_role

def navigation_menu(request):
    sql_role = get_user_sql_role(request)
    all_items = MenuItem.objects.filter(visible=True).select_related('parent').prefetch_related('children')
    menu_tree = []

    # Фільтрація за роллю
    def build_tree(parent=None):
        nodes = [item for item in all_items if item.parent == parent and item.is_allowed_for(sql_role)]
        return [
            {
                'item': item,
                'children': build_tree(item)
            } for item in nodes
        ]

    menu_tree = build_tree()
    return {'navigation_menu': menu_tree}
