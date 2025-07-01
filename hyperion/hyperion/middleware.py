# hyperion/middleware.py
from django.urls import reverse
from users.models import Permition

class PermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        if request.user.is_authenticated and not request.user.is_superuser:
            try:
                allowed_objects = Permition.objects.filter(
                    group_id=request.user.group_id,  # Виправлено: group_id є ForeignKey
                    visible=True
                ).values_list('object_name', flat=True)
                if response.context_data and 'available_apps' in response.context_data:
                    for app in response.context_data['available_apps']:
                        for model in app.get('models', []):
                            model_name = f"{app['app_label']}_{model['object_name'].lower()}"
                            if model_name not in allowed_objects:
                                model['perms']['change'] = False
                                model['perms']['add'] = False
                                model['perms']['delete'] = False
            except Exception as e:
                # Логування помилки (опціонально)
                print(f"Middleware error: {e}")
        return response