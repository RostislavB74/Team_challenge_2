from django.db import models
from django.urls import reverse

class MenuItem(models.Model):
    title = models.CharField(max_length=100, verbose_name="Назва пункту")
    url_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Назва URL (reverse name)")
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE, verbose_name="Батьківський пункт")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    visible = models.BooleanField(default=True, verbose_name="Відображати")
    allowed_roles = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name="SQL-ролі, кому видно (через кому)"
    )

    class Meta:
        # managed = False
        db_table = 'navigation_menuitem'
        ordering = ['order']
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункти меню"

    def __str__(self):
        return self.title

    def is_allowed_for(self, sql_role):
        if not self.allowed_roles:
            return True  # Доступно всім
        allowed = [r.strip() for r in self.allowed_roles.split(',')]
        return sql_role in allowed

    def get_url(self):
        if self.url_name:
            return reverse(self.url_name)
        return None

    # def get_children(self):
    #     return MenuItem.objects.filter(parent=self).order_by('order')

    # def get_ancestors(self):
    #     ancestors = []
    #     parent = self.parent
    #     while parent:
    #         ancestors.append(parent)
    #         parent = parent.parent
    #     return ancestors

    # def get_descendants(self):
    #     return MenuItem.objects.filter(parent=self).order_by('order')