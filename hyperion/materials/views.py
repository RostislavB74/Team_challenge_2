from django.shortcuts import render
from .models import Materials, MaterialGroups, MaterialKinds, MaterialTypes, MaterialUnits
from django.core.paginator import Paginator

def MaterialsListView(request):
    sort = request.GET.get("sort", "id")  # поле для сортування
    direction = request.GET.get("dir", "asc")  # asc / desc

    materials = Materials.objects.all()

    if direction == "desc":
        sort = f"-{sort}"

    materials = materials.order_by(sort)

    paginator = Paginator(materials, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "materials/materials_list.html",
        {
            "page_obj": page_obj,
            "sort": request.GET.get("sort"),
            "dir": request.GET.get("dir"),
        },
    )

   
