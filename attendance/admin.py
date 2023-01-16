from django.contrib import admin
from .models import StatusModel, WorkersModel
from import_export.admin import ImportExportModelAdmin
from import_export import resources
# Register your models here.

# admin.site.register(Workers)
admin.site.register(StatusModel)
# admin.site.register(Attendance)



# class AttendanceProfileAdmin(admin.ModelAdmin):
#     list_display = ['worker','manager','date','mark_attendance']
# admin.site.register(Attendance, AttendanceProfileAdmin)


class WorkerAdmin(ImportExportModelAdmin):
    list_display = ("id", 'worker_name', 'manager_name', "day_off", 'worker_status', 'worker_id')
admin.site.register(WorkersModel,WorkerAdmin)

