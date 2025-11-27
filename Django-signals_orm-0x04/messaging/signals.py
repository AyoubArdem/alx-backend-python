
from django.db.models.signals import post_save , pre_save
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

@receiver(post_delete, sender=User)
def delete_user_related(sender, instance, **kwargs):
    from .models import Message, Notification, MessageHistory

    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    Notification.objects.filter(user=instance).delete()

    MessageHistory.objects.filter(message__sender=instance).delete()

