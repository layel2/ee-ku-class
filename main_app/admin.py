from django.contrib import admin
from main_app.models import sub_list,class_dt,sub_sec,lecturer,semester, update_date,room_db

# Register your models here.
admin.site.register(sub_list)
admin.site.register(class_dt)

admin.site.register(lecturer)
admin.site.register(semester)
admin.site.register(update_date)
admin.site.register(room_db)

class sub_sec_admin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "sub_id":
            kwargs["queryset"] = sub_list.objects.order_by('sub_code','sub_year')
        return super(sub_sec_admin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(sub_sec,sub_sec_admin)