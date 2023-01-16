from django.db import models
from django.contrib.auth.models import Permission, User
from django.urls import reverse
from django.template.defaultfilters import slugify

weekdays = {
    ('Понедельник' ,'Понедельник'),
    ('Вторник','Вторник'),
    ('Среда','Среда'),
    ('Четверг','Четверг'),
    ('Пятница','Пятница'),
    ('Субота','Субота'),
    ('Воскресенье','Воскресенье'),
}
mark_attendance = {
    (1, 'present'),
    (0, 'absent')
}

def get_deleted_user_instance():
    return StatusModel.objects.get(pk=1)

class StatusModel(models.Model):
    status_name = models.CharField(max_length=50, unique=True)
    status_description = models.TextField(max_length=100, blank=True,null=True)

    def __str__(self):
        return f"{self.status_name}"

class WorkersModel(models.Model):
    worker_name = models.CharField(max_length=150, verbose_name='Ф.И.О.', unique=True)
    worker_status = models.ForeignKey(StatusModel, related_name='worker_status', on_delete=models.SET(get_deleted_user_instance), verbose_name="Должность")
    worker_id = models.CharField(max_length=10, verbose_name='Табельный номер',blank=True, null=True)
    day_off = models.CharField(max_length=50, choices=weekdays, verbose_name='Выходной')
    manager_name = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Бригадир')
    present = models.IntegerField(default=0, verbose_name='Была')
    absent = models.IntegerField(default=0, verbose_name="Не была")
    vacation = models.IntegerField(default=0, verbose_name="Всего выходных")
    total = models.FloatField(default=0,verbose_name='Общий рейтинг (%)', blank=True)
    total_hours = models.FloatField(verbose_name='общее количество отработанных часов', blank=True, default=0)
    slug = models.SlugField(blank=True, null=True)



    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.worker_name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.worker_name}"