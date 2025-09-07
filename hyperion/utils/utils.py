# тимчасово або визначай з request.user.username
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q


def get_user_sql_role(request):
    return request.session.get("sql_role", "sysadmin")


def list_view(request, model, template_name, search_fields=None):
    sort = request.GET.get("sort", "id")
    direction = request.GET.get("dir", "asc")
    search = request.GET.get("search", "")

    queryset = model.objects.all()

    # 🔍 Пошук
    if search and search_fields:
        q_objects = Q()
        for field in search_fields:
            q_objects |= Q(**{f"{field}__icontains": search})
        queryset = queryset.filter(q_objects)

    # 🔽 Сортування
    if direction == "desc":
        sort = f"-{sort}"
    queryset = queryset.order_by(sort)

    # 📄 Пагінація
    paginator = Paginator(queryset, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        template_name,
        {
            "page_obj": page_obj,
            "sort": request.GET.get("sort", "id"),
            "dir": request.GET.get("dir", "asc"),
            "search": search,
        },
    )
