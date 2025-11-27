
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def register_old_message(sender,instance):
    if instance.pk:
        old = Message.objects.get(pk=instance.pk)
        if old.content != instance.content:
             MessageHistory.objects.create(
                message=old,
                old_content=old.content
            )
            instance.edited = True
