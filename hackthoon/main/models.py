from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class VisitMonth(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()  # Номер месяца (1 - январь, 12 - декабрь)

    def __str__(self):
        return f"{self.user.username} - {self.year}-{self.month}"

    class Meta:
        unique_together = ('user', 'year', 'month')  # Уникальное сочетание для каждого месяца и пользователя

class DayVisit(models.Model):
    date = models.DateField()
    is_present = models.BooleanField(default=False)  # Отметка о присутствии
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Ссылка на пользователя

    def __str__(self):
        return f"Visit on {self.date} by {self.user}"


class Role(models.Model):
    title = models.CharField(max_length=100, verbose_name='Роль', default=None, null=False)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

class Group(models.Model):
    title = models.CharField(max_length=100, verbose_name='Группа')
    course = models.CharField(max_length=100, verbose_name='Курс')
    
    def __str__(self):
        return f'{self.title} ({self.course})'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, Fio=None, number=None, role=None, **extra_fields):
        if not username:
            raise ValueError('The login must be set')

        if role is None:
            role = Role.objects.get_or_create(title='student')[0]  

        user = self.model(username=username, Fio=Fio, number=number, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, Fio=None, number=None, role=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if role is None:
            role = Role.objects.get_or_create(title='admin')[0]

        return self.create_user(username, password, Fio=Fio, number=number, role=role, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    Fio = models.CharField(max_length=255, null=True, blank=True, verbose_name="ФИО")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Группа")
    number = models.CharField(max_length=15, null=True, blank=True)
    numberFamily = models.CharField(max_length=15, null=True, blank=True)
    Email = models.EmailField(blank=True, null=True)
    EmailFamily = models.EmailField(blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, default=1, verbose_name="Роль")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # Новое поле для подсчета пропусков
    absent_count = models.PositiveIntegerField(default=0, verbose_name="Количество пропусков")

    # Метод для расчета процента посещаемости
    def attendance_percentage(self):
        total_days = self.attendance_records.count()  # Общее количество записей
        if total_days == 0:
            return 0  # Если записей нет, посещаемость равна 0%
        present_days = total_days - self.absent_count  # Присутствующие дни
        return round((present_days / total_days) * 100, 2)  # Процент

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

class AttendanceRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField(verbose_name="Дата")
    status = models.CharField(
        max_length=10,
        choices=[
            ('present', 'Присутствовал'),
            ('absent', 'Отсутствовал'),
            ('none', 'Не указано'),
        ],
        default='none',
        verbose_name="Статус посещения"
    )

    def __str__(self):
        return f"{self.user.username} - {self.date} ({self.status})"


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE, 
        related_name='profile'     
    )
    Fio = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    course = models.CharField(max_length=50, blank=True, null=True)
    number = models.CharField(max_length=20, blank=True, null=True)
    numberFamily = models.CharField(max_length=20, blank=True, null=True)
    Email = models.EmailField(blank=True, null=True)


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save() 
