# from django.urls import path
# from django.views.generic import TemplateView


# urlpatterns = [
#     path('', TemplateView.as_view(template_name="home.html"), name='home'),
# ]


from django.urls import path
from .views import menu_view


urlpatterns = [
    path('', menu_view, name='menu_home'),
    # path('dovidniki/', dovidniki_view, name='dovidniki'),
    # path('dovidniki/', dovidniki_home, name='dovidniki'),
]
app_name = 'navigation'
