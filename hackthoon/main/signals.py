from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import AttendanceRecord, CustomUser, UserProfile

@receiver(post_save, sender=AttendanceRecord)
@receiver(post_delete, sender=AttendanceRecord)
def update_absent_count(sender, instance, **kwargs):
    # Получаем пользователя, связанного с записью
    user = instance.user

    # Считаем количество записей с `status='absent'` для данного пользователя
    absent_count = AttendanceRecord.objects.filter(user=user, status='absent').count()

    # Обновляем поле `absent_count`
    user.absent_count = absent_count
    user.save()

@receiver(post_save, sender=CustomUser)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
