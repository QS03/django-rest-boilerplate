from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    exclude = []

    def get_list_display(self, request):
        list_display = [
            field.name for field in self.model._meta.concrete_fields if field.name not in self.exclude
        ]
        return list_display

    class Meta:
        abstract = True
